import asyncio
import json
from typing import Any, Dict, List, Optional, Sequence
import logging

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

# Your existing imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
import yfinance as yf
import os
import ast
import warnings
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings("ignore", message="API key must be provided when using hosted LangSmith API")

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance-agent")

# Your existing tool (with slight modifications for better error handling)
@tool
def get_stock_prices(tickers: str) -> str:
    """
    Fetches the current stock prices for a list of ticker symbols.
    The input should be a string representation of a Python list (e.g., "['GOOG', 'MSFT']").
    Returns the prices in the stock's native currency (USD for US, INR for Indian).
    """
    results = []
    try:
        ticker_list = ast.literal_eval(tickers)
        if not isinstance(ticker_list, list):
            return "Input must be a list of ticker symbols."
    except (ValueError, SyntaxError):
        return "Invalid input format. Please provide a list of tickers as a string (e.g., \"['GOOG', 'RELIANCE.NS']\")."
    
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            price = stock.info.get('regularMarketPrice')
            if price is None:
                price = stock.history(period="1d")['Close'].iloc[-1]
            currency = stock.info.get('currency', 'USD')
            results.append(f"The current price of {ticker} is {price:.2f} {currency}. ")
        except Exception as e:
            results.append(f"Could not find the stock price for {ticker}. Error: {e}. ")
    
    return "".join(results)

class FinanceAgentServer:
    def __init__(self):
        self.google_api_key = os.getenv("GEMINI_API_KEY")
        self.model = "models/gemini-2.5-flash-lite-preview-06-17"
        
        if not self.google_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize the LangChain components
        self.llm = ChatGoogleGenerativeAI(model=self.model, google_api_key=self.google_api_key)
        self.tools = [get_stock_prices]
        self.prompt = hub.pull("hwchase17/react")
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True
        )

    async def query_agent(self, query: str) -> str:
        """Execute a query using the LangChain agent"""
        try:
            response = self.agent_executor.invoke({"input": query})
            return response["output"]
        except Exception as e:
            logger.error(f"Error executing agent query: {e}")
            return f"Error: {str(e)}"

# Create the MCP server
server = Server("finance-agent")
finance_server = FinanceAgentServer()

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_stock_prices",
            description="Get current stock prices for a list of ticker symbols. Input should be a list of tickers like ['GOOG', 'MSFT', 'RELIANCE.NS']",
            inputSchema={
                "type": "object",
                "properties": {
                    "tickers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock ticker symbols (e.g., ['GOOG', 'MSFT', 'RELIANCE.NS'])"
                    }
                },
                "required": ["tickers"]
            }
        ),
        Tool(
            name="finance_agent_query",
            description="Ask the finance agent any question about stocks, market analysis, or financial data. The agent can fetch stock prices and provide analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Your question about stocks or financial markets"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls"""
    
    if name == "get_stock_prices":
        try:
            tickers = arguments.get("tickers", [])
            if not tickers:
                return [TextContent(type="text", text="Error: No tickers provided")]
            
            # Convert list to string format expected by the original tool
            tickers_str = str(tickers)
            result = get_stock_prices(tickers_str)
            
            return [TextContent(type="text", text=result)]
        
        except Exception as e:
            logger.error(f"Error in get_stock_prices: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "finance_agent_query":
        try:
            query = arguments.get("query", "")
            if not query:
                return [TextContent(type="text", text="Error: No query provided")]
            
            result = await finance_server.query_agent(query)
            return [TextContent(type="text", text=result)]
        
        except Exception as e:
            logger.error(f"Error in finance_agent_query: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Error: Unknown tool {name}")]

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="finance://agent/info",
            name="Finance Agent Info",
            description="Information about the finance agent capabilities",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a resource"""
    if uri == "finance://agent/info":
        return """Finance Agent MCP Server

This server provides access to a LangChain-powered finance agent that can:

1. Fetch current stock prices for any ticker symbols
2. Answer questions about stocks and financial markets
3. Provide market analysis using real-time data

Available tools:
- get_stock_prices: Get current prices for specific stocks
- finance_agent_query: Ask any finance-related question

Supported markets:
- US stocks (e.g., GOOG, MSFT, AAPL)
- Indian stocks (add .NS suffix, e.g., RELIANCE.NS)
- Other international markets (use appropriate suffix)

Example queries:
- "What's the current price of Apple stock?"
- "Compare Google and Microsoft stock prices"
- "Give me analysis of tech stocks today"
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")

async def main():
    """Main server loop"""
    logger.info("Starting Finance Agent MCP Server...")
    
    # Verify environment setup
    try:
        finance_server  # This will trigger initialization
        logger.info("Finance agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize finance agent: {e}")
        return
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())