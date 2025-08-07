import os
import asyncio
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import StructuredTool

load_dotenv()
api_key = "ollama"
model_name = "llama3.1:8b"

server_params = StdioServerParameters(command="python", args=["calculator_server.py"])

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate")

async def main():
    async with stdio_client(server_params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()

            tools = []
            for t in (await session.list_tools()).tools:
                async def tool_fn(input, tool_name=t.name):
                    expr = input.expression if hasattr(input, "expression") else str(input)
                    result = await session.call_tool(tool_name, {"expression": expr})
                    if hasattr(result, "structured_content") and result.structured_content is not None:
                        return result.structured_content
                    return "".join(getattr(block, "text", "") for block in result.content)

                structured_tool = StructuredTool.from_function(
                    func=None,
                    coroutine=tool_fn,
                    name=t.name,
                    description=t.description or "Execute a calculation",
                    args_schema=CalculatorInput,
                    return_direct=True,
                )
                tools.append(structured_tool)

            llm = ChatOllama(model=model_name, api_key=api_key)

            agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True)

            prompt = "What is 25 * 25?"
            result = await agent.ainvoke({"input": prompt})
            print("Agent Response:", result.get("output", result))

if __name__ == "__main__":
    asyncio.run(main())
