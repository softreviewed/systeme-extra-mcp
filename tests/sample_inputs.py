"""Build minimal schema-valid inputs for every documented operation (used for offline preview tests)."""

from server import resolve


def sample(schema, spec, depth=0):
    schema = resolve(schema, spec) or {}
    if depth > 8:
        return None
    for key in ("oneOf", "anyOf"):
        if key in schema:
            options = [o for o in schema[key] if resolve(o, spec).get("type") != "null"]
            return sample(options[0], spec, depth + 1)
    if "allOf" in schema:
        merged = {}
        for part in schema["allOf"]:
            value = sample(part, spec, depth + 1)
            if isinstance(value, dict):
                merged.update(value)
        return merged
    if "enum" in schema:
        return next((v for v in schema["enum"] if v is not None), None)
    if "const" in schema:
        return schema["const"]
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next((k for k in kind if k != "null"), "string")
    if kind == "object" or "properties" in schema:
        return {name: sample(schema["properties"][name], spec, depth + 1)
                for name in schema.get("required", []) if name in schema.get("properties", {})}
    if kind == "array":
        count = schema.get("minItems", 0)
        return [sample(schema.get("items", {}), spec, depth + 1) for _ in range(count)]
    if kind == "integer":
        return max(1, schema.get("minimum", 1))
    if kind == "number":
        return max(1, schema.get("minimum", 1))
    if kind == "boolean":
        return True
    fmt = schema.get("format")
    if fmt == "email":
        return "test@example.com"
    if fmt in ("uri", "url"):
        return "https://example.com/hook"
    if fmt == "date-time":
        return "2026-10-13T10:00:00+00:00"
    if fmt == "date":
        return "2026-10-13"
    if fmt == "time":
        return "10:00:00"
    if fmt == "uuid":
        return "123e4567-e89b-12d3-a456-426614174000"
    return "x" * max(1, schema.get("minLength", 7)) if not schema.get("pattern") else None


def inputs(entry):
    op, spec = entry["operation"], entry["spec"]
    params = {p["name"]: sample(p.get("schema", {}), spec) for p in op.get("parameters", []) if p.get("required")}
    body = None
    content = op.get("requestBody", {}).get("content", {})
    if content:
        body = sample(next(iter(content.values())).get("schema", {}), spec)
    return params, body
