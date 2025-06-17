from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """
    __get the weather details___


    
    """

    return "it's always rains in the chittor location"


if __name__=="__main__":
    mcp.run(transport="streamable-http")