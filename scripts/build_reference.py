"""Regenerate the action table in docs/feature-reference.md from docs/operations.json."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server import GROUPS, HIGH_IMPACT, OPERATIONS, is_write  # noqa: E402

START, END = "<!-- actions:start -->", "<!-- actions:end -->"


def inputs(entry):
    op = entry["operation"]
    required = [p["name"] for p in op.get("parameters", []) if p.get("required")]
    body = op.get("requestBody", {}).get("content")
    parts = [f"`{name}`" for name in required]
    if body:
        parts.append("body")
    return ", ".join(parts) or "None"


def table():
    lines = [START, ""]
    for group, description in GROUPS.items():
        lines += [f"### {group}", "", description, "",
                  "| Action | Method | Path | Required input | Type |", "|---|---|---|---|---|"]
        for (domain, action), entry in sorted(OPERATIONS.items()):
            if domain != group:
                continue
            kind = "High-impact write" if (domain, action) in HIGH_IMPACT else ("Write" if is_write(domain, action) else "Read")
            lines.append(f"| `{action}` | {entry['method']} | `{entry['path']}` | {inputs(entry)} | {kind} |")
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


def main():
    path = ROOT / "docs" / "feature-reference.md"
    text = path.read_text(encoding="utf-8")
    start, end = text.index(START), text.index(END) + len(END)
    path.write_text(text[:start] + table() + text[end:], encoding="utf-8")
    print(f"{len(OPERATIONS)} actions written to {path.name}")


if __name__ == "__main__":
    main()
