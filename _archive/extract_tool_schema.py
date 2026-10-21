"""Deterministic tool-schema extractor (AST-only, no LLM).

Resolves `CoreTool.from_function(...)` / `<X>.from_function(...)` call sites to
their wrapped function's signature and docstring via a cross-file AST index,
then emits a JSON Schema per tool.

Annotation handling (vs the runtime `CoreTool.parameters`):
- PEP 604 unions (`int | None`) and `Optional`/`Union[..., None]` collapse to the
  single non-None arm.
- `list[X]` / `Sequence[X]` -> `array` with `items`.
- `dict[K, V]` / `Mapping[K, V]` -> `object` with `additionalProperties`.
- Parameter descriptions are read deterministically from the Google-style
  `Args:` section of the docstring (mirrors `_extract_parameter_descriptions_from_docstring`).

Usage:
    py extract_tool_schema.py [ROOT_DIR]
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(
    r"d:\My Docunments\AI\artifacts-report\_archive\_clones\opencontracts"
    r"\opencontractserver\llms\tools"
)

_PRIMITIVES = {
    "int": "integer",
    "Integer": "integer",
    "float": "number",
    "double": "number",
    "Decimal": "number",
    "bool": "boolean",
    "boolean": "boolean",
    "str": "string",
    "Text": "string",
    "Any": "object",
    "object": "object",
}

_LIST_BASES = {"list", "List", "Sequence", "MutableSequence"}
_DICT_BASES = {"dict", "Dict", "Mapping", "MutableMapping"}
_TUPLE_BASES = {"tuple", "Tuple"}
_OPTIONAL_BASES = {"Optional", "Union"}


def _node_name(node: ast.expr) -> str | None:
    """Return the base identifier of an annotation node, or None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _is_none(node: ast.expr) -> bool:
    name = _node_name(node)
    return name in ("None", "NoneType") or (
        isinstance(node, ast.Constant) and node.value is None
    )


def _slice_elements(slice_node: ast.expr) -> list[ast.expr]:
    """Flatten a Subscript slice into element expressions."""
    if isinstance(slice_node, ast.Tuple):
        return list(slice_node.elts)
    return [slice_node]


def _flatten_union(node: ast.expr) -> list[ast.expr]:
    """Flatten a PEP 604 `X | Y | Z` expression into its arms."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _flatten_union(node.left) + _flatten_union(node.right)
    return [node]


def annotation_to_schema(node: ast.expr | None) -> dict:
    """Recursively convert an annotation AST node to a JSON Schema fragment."""
    if node is None:
        return {"type": "string"}

    # PEP 604 union: int | None, str | int, dict[str,int] | None, ...
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        arms = _flatten_union(node)
        non_none = [a for a in arms if not _is_none(a)]
        if len(non_none) == 1:
            return annotation_to_schema(non_none[0])
        # Multiple non-None arms -> not expressible in this simple schema.
        return {"type": "string"}

    # Subscript: list[X], dict[K,V], Optional[X], Union[X, None], ...
    if isinstance(node, ast.Subscript):
        base = _node_name(node.value)
        elems = _slice_elements(node.slice)

        if base in _OPTIONAL_BASES:
            non_none = [e for e in elems if not _is_none(e)]
            if len(non_none) == 1:
                return annotation_to_schema(non_none[0])
            return {"type": "string"}

        if base in _LIST_BASES:
            schema: dict = {"type": "array"}
            if len(elems) == 1:
                schema["items"] = annotation_to_schema(elems[0])
            return schema

        if base in _TUPLE_BASES:
            return {"type": "array"}

        if base in _DICT_BASES:
            schema = {"type": "object"}
            if len(elems) == 2:
                schema["additionalProperties"] = annotation_to_schema(elems[1])
            return schema

        return {"type": "string"}

    # Plain name / attribute: int, str, bool, list, dict, custom.Type, ...
    name = _node_name(node)
    if name in _PRIMITIVES:
        return {"type": _PRIMITIVES[name]}
    return {"type": "string"}


def _extract_param_descriptions(doc: str | None) -> dict[str, str]:
    """Deterministically parse the `Args:` section of a Google-style docstring."""
    if not doc:
        return {}
    out: dict[str, str] = {}
    in_args = False
    for raw in doc.split("\n"):
        line = raw.strip()
        if line.startswith("Args:") or line.startswith("Arguments:"):
            in_args = True
            continue
        if line.startswith("Returns:") or line.startswith("Raises:"):
            in_args = False
            continue
        if in_args and ":" in line:
            name, _, desc = line.partition(":")
            out[name.strip()] = desc.strip()
    return out


def _first_line(doc: str | None) -> str:
    if not doc:
        return ""
    return doc.strip().split("\n", 1)[0].strip()


def scan(root: Path) -> dict:
    func_index: dict[str, dict] = {}
    calls: list[dict] = []

    for py in sorted(root.rglob("*.py")):
        if py.name == "__init__.py":
            continue
        try:
            src = py.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                n_args = node.args.args
                defaults = [None] * (len(n_args) - len(node.args.defaults)) + list(
                    node.args.defaults
                )
                sig = []
                for a, d in zip(n_args, defaults):
                    sig.append(
                        {
                            "name": a.arg,
                            "annotation": a.annotation,
                            "required": d is None,
                        }
                    )
                func_index[node.name] = {
                    "file": str(py),
                    "sig": sig,
                    "doc": ast.get_docstring(node),
                }

            if isinstance(node, ast.Call):
                f = node.func
                if isinstance(f, ast.Attribute) and f.attr == "from_function":
                    kw: dict = {}
                    for kwarg in node.keywords:
                        if kwarg.arg in ("name", "description"):
                            v = kwarg.value
                            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                                kw[kwarg.arg] = v.value
                    func_ref = None
                    if node.args:
                        a0 = node.args[0]
                        if isinstance(a0, ast.Name):
                            func_ref = a0.id
                        elif isinstance(a0, ast.Attribute):
                            func_ref = a0.attr
                    calls.append(
                        {"file": str(py), "line": node.lineno, "func_ref": func_ref, **kw}
                    )

    tools: list[dict] = []
    unresolved: list[dict] = []
    for c in calls:
        ref = c.get("func_ref")
        info = func_index.get(ref) if ref else None
        if info is None:
            unresolved.append(c)
            continue
        name = c.get("name") or (info and ref) or (ref or "<unknown>")
        desc = c.get("description") or _first_line(info.get("doc"))
        param_descs = _extract_param_descriptions(info.get("doc"))

        props = {}
        required = []
        for p in info["sig"]:
            schema = annotation_to_schema(p["annotation"])
            schema["description"] = param_descs.get(p["name"], "")
            props[p["name"]] = schema
            if p["required"]:
                required.append(p["name"])

        tools.append(
            {
                "name": name,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required,
                },
                "source": f"{c['file']}:{c['line']}",
                "func": ref,
            }
        )

    seen: dict[str, dict] = {}
    for t in tools:
        seen.setdefault(t["name"], t)

    return {
        "root": str(root),
        "call_sites_found": len(calls),
        "tools_resolved": len(seen),
        "unresolved": len(unresolved),
        "unresolved_calls": unresolved,
        "tools": list(seen.values()),
    }


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    print(json.dumps(scan(root), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
