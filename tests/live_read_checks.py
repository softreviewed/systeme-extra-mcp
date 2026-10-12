"""Authenticated read-only checks; output metadata only, never customer data."""
import asyncio
import datetime
import json
import os
import shutil
import sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main():
    root = Path(__file__).resolve().parents[1]
    catalog = os.getenv("SYSTEME_EXTRA_CATALOG", str(root / "docker-catalog.yaml"))
    transport = StdioTransport(command=shutil.which("docker"), args=["mcp", "gateway", "run", "--catalog",
        catalog, "--servers", "systeme-extra", "--log-calls=false"], env=dict(os.environ))
    sys.path.insert(0, str(root))
    from server import OPERATIONS, is_write
    # Every GET that needs no path or query input: safe inventory reads across all groups.
    checks = [key for key, entry in OPERATIONS.items() if not is_write(*key) and entry["method"] == "GET"
              and not any(p.get("required") for p in entry["operation"].get("parameters", []))]
    rows = []
    contact_id = None
    async with Client(transport) as client:
        for domain, action in checks:
            result = await client.call_tool("systeme_extra_" + domain, {"action": action})
            data = result.data
            rows.append({"tool": domain, "action": action, "ok": data.get("ok"),
                         "status": data.get("status"), "error": data.get("error")})
            if domain in ("enrolments", "communities", "contacts") and data.get("ok") and not contact_id:
                items = data.get("data", {}).get("items", []) if isinstance(data.get("data"), dict) else []
                for item in items:
                    contact = item if domain == "contacts" else item.get("contact")
                    if isinstance(contact, dict) and isinstance(contact.get("id"), int):
                        contact_id = contact["id"]
                        break
        if contact_id:
            result = await client.call_tool("systeme_extra_subscriptions", {"action": "list", "parameters": {"contact": contact_id}})
            rows.append({"tool": "subscriptions", "action": "list", "ok": result.data.get("ok"), "status": result.data.get("status")})
        else:
            rows.append({"tool": "subscriptions", "action": "list", "skipped": "No contact identifier returned by tested collections; no ID guessed."})
    output = {"date": datetime.date.today().isoformat(), "mode": "read-only", "writes_performed": 0, "checks": rows}
    (Path(__file__).parent.parent / "docs/live-read-results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
