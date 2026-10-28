#!/usr/bin/env python3
"""Verify the Energy Management Assistant can be imported and initialized."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test all critical imports work."""
    print("Testing imports...")

    # Test sanityops_agent
    try:
        from sanityops_agent import (
            AgentFactory,
            ToolRegistry,
            Tool,
            ToolResult,
            ToolContext,
            ProviderConfig,
        )
        print("  ✓ sanityops_agent imports OK")
    except ImportError as e:
        print(f"  ✗ sanityops_agent import failed: {e}")
        return False

    # Test API
    try:
        from apis.energy_api import login, ROLE_PERMISSIONS
        print("  ✓ apis.energy_api imports OK")
    except ImportError as e:
        print(f"  ✗ apis.energy_api import failed: {e}")
        return False

    # Test DataStore
    try:
        from apis.data_store import DataStore
        print("  ✓ apis.data_store imports OK")
    except ImportError as e:
        print(f"  ✗ apis.data_store import failed: {e}")
        return False

    # Test all tools
    tools_dir = project_root / "tools"
    for tool_file in tools_dir.glob("energy_*.py"):
        tool_name = tool_file.stem
        try:
            module = __import__(f"tools.{tool_name}", fromlist=["execute"])
            if not hasattr(module, "execute"):
                print(f"  ✗ {tool_name} has no execute function")
                return False
            print(f"  ✓ tools.{tool_name} OK")
        except ImportError as e:
            print(f"  ✗ tools.{tool_name} import failed: {e}")
            return False

    # Test all skill handlers
    skills_dir = project_root / "skills"
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith("_"):
            try:
                handler_file = skill_dir / "handler.py"
                if handler_file.exists():
                    module_name = f"skills.{skill_dir.name}.handler"
                    module = __import__(module_name, fromlist=["run"])
                    if not hasattr(module, "run"):
                        print(f"  ✗ {skill_dir.name} handler has no run function")
                        return False
                    print(f"  ✓ skills.{skill_dir.name}.handler OK")
            except ImportError as e:
                print(f"  ✗ skills.{skill_dir.name} import failed: {e}")
                return False

    return True


def test_tool_execution():
    """Test tools can be executed."""
    print("\nTesting tool execution...")

    from tools.energy_analyze_consumption import execute as analyze
    from tools.energy_recommend_optimizations import execute as recommend

    result = analyze({
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-07"
    })

    if result["status"] != "success":
        print(f"  ✗ energy_analyze_consumption failed: {result.get('error')}")
        return False
    print("  ✓ energy_analyze_consumption executes OK")

    result = recommend({"facility_id": "FAC001"})
    if result["status"] != "success":
        print(f"  ✗ energy_recommend_optimizations failed: {result.get('error')}")
        return False
    print("  ✓ energy_recommend_optimizations executes OK")

    return True


def test_skill_handlers():
    """Test skill handlers route correctly."""
    print("\nTesting skill handlers...")

    from skills.energy_analysis.handler import run as energy_run

    # Test valid intent
    result = energy_run("analyze_consumption", {
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-07"
    })
    if result["status"] != "success":
        print(f"  ✗ energy_analysis handler failed: {result.get('error')}")
        return False
    print("  ✓ energy_analysis handler OK")

    # Test invalid intent
    result = energy_run("invalid_intent", {})
    if result["status"] == "success":
        print("  ✗ energy_analysis should fail on invalid intent")
        return False
    print("  ✓ energy_analysis rejects invalid intent OK")

    return True


def test_data_loading():
    """Test DataStore can load data."""
    print("\nTesting DataStore...")

    from apis.data_store import DataStore

    data_store = DataStore(data_dir=project_root / "data")

    facilities = data_store.load_facilities()
    if not facilities:
        print("  ✗ No facilities loaded")
        return False
    print(f"  ✓ Loaded {len(facilities)} facilities")

    equipment = data_store.load_equipment()
    if not equipment:
        print("  ✗ No equipment loaded")
        return False
    print(f"  ✓ Loaded {len(equipment)} equipment records")

    return True


def test_provider_config():
    """Test ProviderConfig loads from .env."""
    print("\nTesting ProviderConfig...")

    from sanityops_agent import ProviderConfig

    config = ProviderConfig()
    if not config.API_KEY:
        print("  ⚠ API_KEY not configured (this is OK for testing)")
    else:
        print(f"  ✓ API_KEY configured: {config.API_KEY[:10]}...")

    return True


def main():
    print("=" * 50)
    print("Energy Management Assistant - Verification")
    print("=" * 50)
    print()

    all_passed = True

    all_passed &= test_imports()
    all_passed &= test_data_loading()
    all_passed &= test_tool_execution()
    all_passed &= test_skill_handlers()
    all_passed &= test_provider_config()

    print()
    print("=" * 50)
    if all_passed:
        print("✅ All verification checks passed!")
        print()
        print("The agent is ready to run with:")
        print("  python scripts/run.py")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()