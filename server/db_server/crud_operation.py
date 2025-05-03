from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# 1. Initialize FastMCP server
mcp = FastMCP("crud")

# Constants
DB_API_BASE = "http://localhost:8000"
USER_AGENT = "crud-app/1.0"

# make sure you have mcp installed on venv : pip install mcp

# User input
class UserInput(BaseModel):
    user_query: str

    
# 2. Helper function for querying and formatting
async def make_db_request(url: str, user_query: str) -> dict[str, Any] | None:
    """Make a request to a Database with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "user_query": user_query
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Use POST since we're sending data
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

@mcp.tool()
async def get_data(input: UserInput):
    """ Database CRUD operationss
    """
    
    url = f"{DB_API_BASE}/crud/"
    data = await make_db_request(url, input.user_query)

    if not data:
        return "Unable to fetch data from database."

    return data

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')