"""Read-only tool discovery and help checks through the real Docker Gateway."""
import asyncio
import os
import shutil
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main():
    catalog = os.getenv("SYSTEME_EXTRA_CATALOG", str(Path(__file__).resolve().parents[1] / "docker-catalog.yaml"))
    transport = StdioTransport(command=shutil.which("docker"), args=["mcp", "gateway", "run", "--catalog", catalog,
                                                       "--servers", "systeme-extra", "--log-calls=false"], env=dict(os.environ))
    async with Client(transport) as client:
        tools = await client.list_tools()
        assert len(tools) == 6, len(tools)
        count = 0
        for tool in tools:
            result = await client.call_tool(tool.name, {"action": "help"})
            assert not result.is_error, tool.name
            data = result.data
            assert isinstance(data, dict) and "actions" in data, tool.name
            count += len(data["actions"])
        assert count == 20, count
        preview = await client.call_tool("systeme_extra_enrolments", {
            "action": "create", "parameters": {"courseId": 123},
            "body": {"contactId": 456, "accessType": "full_access"}, "dry_run": True})
        assert preview.data["dry_run"] is True
        print("Gateway verified: 6 tools, 20 operations, and write preview; no API requests sent.")


if __name__ == "__main__":
    asyncio.run(main())
