import sqlite3
from mcp import McpServer, Tool

@Tool
def query_db(query: str) -> str:
    """
    Executes a SQL query on the database.
    """
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    server = McpServer(tools=[query_db])
    server.run()
