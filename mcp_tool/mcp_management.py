

from fastmcp import Client
import json

class McpTool:
    
    def __init__(self, mcp_file_path):
        self.tools_allowed = {}
        self.is_tool_from_mcp_server = {}
        self.mcp_tools = []
        self.mcp_file_path = mcp_file_path
        self.mcp_config = {}
        
    def get_tools_allowed(self):
        return self.tools_allowed

    def get_is_tool_from_mcp_server(self):
        return self.is_tool_from_mcp_server
    
    def get_mcp_tools(self):
        return self.mcp_tools
    
    
    async def run_tool(self, name, args):
        async with Client(self.mcp_config) as client:
            res = await client.call_tool(name=name, arguments=args)  
            return (res.content[0].text)
        
    async def load_mpc_tools(self):
        if self.mcp_file_path == None:
            return
        
        with open(self.mcp_file_path, "r") as f:
            file_content_string = f.read(1000000)
            self.mcp_config = json.loads(file_content_string)
            async with Client(self.mcp_config) as client:
                tools = (await client.list_tools())
                for tool in tools:
                    self.is_tool_from_mcp_server[f'{tool.name}'] = True;
                    self.tools_allowed[f'{tool.name}'] = True
                    self.mcp_tools.append(
                        {
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": (tool.inputSchema)
                            }
                        }
                    )
                
            
    