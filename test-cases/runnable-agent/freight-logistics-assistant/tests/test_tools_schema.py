"""Tests for tools schema consistency."""

import sys
import json
from pathlib import Path
import pytest

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestToolsSchema:
    """Verify tools_schema.json matches tool definitions."""

    def test_tools_schema_exists(self):
        """Check tools_schema.json exists."""
        schema_path = project_root / "tools_schema.json"
        assert schema_path.exists(), "tools_schema.json not found"

    def test_tools_schema_valid_json(self):
        """Check tools_schema.json is valid JSON."""
        schema_path = project_root / "tools_schema.json"
        with open(schema_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 9  # We have 9 tools

    def test_all_tools_have_schema(self):
        """Check all tool files have parameters."""
        tools_dir = project_root / "tools"

        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name.startswith("_"):
                continue

            # Import the module
            tool_name = tool_file.stem
            import importlib.util
            spec = importlib.util.spec_from_file_location(tool_name, tool_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check it has parameters
            assert hasattr(module, "parameters"), f"{tool_name} missing parameters"
            assert hasattr(module, "execute"), f"{tool_name} missing execute"
            assert isinstance(module.parameters, dict), f"{tool_name} parameters not dict"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])