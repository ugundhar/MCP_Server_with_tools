from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import asyncio
import os

# Load environment variables
load_dotenv()

async def main():
    # Setup the MCP client with math and weather tools
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],  # Make sure the path is correct
                "transport": "stdio"
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable-http"
            }
        }
    )

    # Set the GROQ API key from environment variable
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Get available tools
    tools = await client.get_tools()

    # Initialize the ChatGroq model
    model = ChatGroq(model="qwen-qwq-32b")

    # Create a ReAct agent with the model and tools
    agent = create_react_agent(model, tools)

    # Math query
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is (3+5) x 12?"}]}
    )
    print("Math response:", math_response['messages'][-1]['content'])

    # Weather query
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in Chittoor?"}]}
    )
    print("Weather response:", weather_response['messages'][-1]['content'])

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
