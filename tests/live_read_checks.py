"""Authenticated read-only checks; output metadata only, never customer data."""
import asyncio
import json
import os
import shutil
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main():
    transport = StdioTransport(command=shutil.which("docker"), args=["mcp", "gateway", "run", "--catalog",
        "custom.yaml", "--servers", "systeme-extra", "--log-calls=false"], env=dict(os.environ))
    checks = [("enrolments", "list"), ("communities", "list"), ("communities", "list_members"),
              ("webhooks", "list"), ("sms", "services"), ("sms", "numbers"), ("sms", "twilio_account")]
    rows = []
    contact_id = None
    async with Client(transport) as client:
        for domain, action in checks:
            result = await client.call_tool("systeme_extra_" + domain, {"action": action})
            data = result.data
            rows.append({"tool": domain, "action": action, "ok": data.get("ok"),
                         "status": data.get("status"), "error": data.get("error")})
            if domain in ("enrolments", "communities") and data.get("ok"):
                items = data.get("data", {}).get("items", []) if isinstance(data.get("data"), dict) else []
                for item in items:
                    contact = item.get("contact")
                    if isinstance(contact, dict) and isinstance(contact.get("id"), int):
                        contact_id = contact["id"]
        if contact_id:
            result = await client.call_tool("systeme_extra_subscriptions", {"action": "list", "parameters": {"contact": contact_id}})
            rows.append({"tool": "subscriptions", "action": "list", "ok": result.data.get("ok"), "status": result.data.get("status")})
        else:
            rows.append({"tool": "subscriptions", "action": "list", "skipped": "No contact identifier returned by tested collections; no ID guessed."})
    output = {"date": "2026-10-06", "mode": "read-only", "writes_performed": 0, "checks": rows}
    (Path(__file__).parent.parent / "docs/live-read-results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
