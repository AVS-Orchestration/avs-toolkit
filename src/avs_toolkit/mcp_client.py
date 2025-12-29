import asyncio
import os
from typing import Dict, List, Any, Optional, Tuple
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

from .models import MCPServerConfig

class MCPRuntime:
    """
    Orchestrates the lifecycle of ephemeral MCP servers.
    Manages connections, tool execution, and resource cleanup.
    """
    def __init__(self, server_configs: List[MCPServerConfig]):
        self.configs = {cfg.name: cfg for cfg in server_configs}
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()

    async def _get_session(self, server_name: str) -> ClientSession:
        """
        Connects to an MCP server on-demand if not already connected.
        Uses StdioServerParameters to launch the subprocess.
        """
        if server_name in self.sessions:
            return self.sessions[server_name]

        if server_name not in self.configs:
            raise ValueError(f"MCP Server '{server_name}' not found in manifest.")

        config = self.configs[server_name]
        
        # Configure the subprocess parameters
        server_params = StdioServerParameters(
            command=config.command,
            args=config.args,
            env={**os.environ, **(config.env or {})}
        )

        # Use the AsyncExitStack to ensure the stdio transport is closed later
        transport_ctx = stdio_client(server_params)
        read_stream, write_stream = await self.exit_stack.enter_async_context(transport_ctx)
        
        session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        
        self.sessions[server_name] = session
        return session

    async def call_tool(self, server_name: str, tool_name: str, tool_args: Dict[str, Any]) -> str:
        """
        Executes a specific tool call on a managed MCP server.
        Returns the text result of the tool execution.
        """
        try:
            session = await self._get_session(server_name)
            result = await session.call_tool(tool_name, arguments=tool_args)
            
            # MCP results can contain multiple content types; we extract the text
            text_outputs = [
                content.text for content in result.content 
                if hasattr(content, 'text') and content.text
            ]
            
            if not text_outputs:
                return f"Warning: Tool '{tool_name}' returned no text content."
                
            return "\n".join(text_outputs)
            
        except Exception as e:
            return f"Error calling MCP tool '{tool_name}' on server '{server_name}': {str(e)}"

    async def shutdown(self):
        """
        Closes all active server sessions and transports.
        """
        await self.exit_stack.aclose()
        self.sessions.clear()

async def execute_mcp_item(runtime: MCPRuntime, item: Any, server_map: Dict[str, str]) -> str:
    """
    Helper to route a ContextManifestItem to the correct MCP server and tool.
    Uses the tool name to look up which server provides it if not explicitly mapped.
    """
    if not item.mcp_tool_name:
        return "Error: No MCP tool name provided for this context item."

    # In a simple implementation, we assume the user maps tools to servers in their manifest
    # or we search the available servers. For now, we look for a server that provides the tool.
    # Architecture Note: In the future, we could call 'list_tools' on all servers to auto-discover.
    
    server_name = None
    for s_name in runtime.configs.keys():
        # Heuristic: The user often prefixes tool names or we can just try the first available
        # if the manifest is simple. For the Firecrawl example, we expect one server.
        server_name = s_name
        break

    if not server_name:
        return "Error: No MCP servers available to handle tool call."

    return await runtime.call_tool(
        server_name=server_name,
        tool_name=item.mcp_tool_name,
        tool_args=item.mcp_tool_args or {}
    )