"""Integration tests for Energy Management Assistant."""

import sys
from pathlib import Path
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_data_files_exist():
    """Test that required data files exist."""
    data_dir = project_root / "data"

    required_files = [
        "facilities.json",
        "equipment.json",
        "consumption_patterns.json",
        "efficiency_measures.json",
        "renewable_options.json"
    ]

    for filename in required_files:
        filepath = data_dir / filename
        assert filepath.exists(), f"Missing data file: {filename}"

        # Verify JSON is valid
        with open(filepath) as f:
            data = json.load(f)
            assert data, f"Empty data file: {filename}"

    print("✓ data files test passed")


def test_energy_analyze_consumption():
    """Test consumption analysis tool."""
    from tools.energy_analyze_consumption import execute

    result = execute({
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-07"
    })

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert "data" in result
    assert result["data"]["facility_id"] == "FAC001"
    assert result["data"]["total_consumption_kwh"] > 0
    assert "patterns" in result["data"]
    print("✓ energy_analyze_consumption test passed")


def test_energy_identify_efficiency_opportunities():
    """Test opportunity identification tool."""
    from tools.energy_identify_efficiency_opportunities import execute

    result = execute({"facility_id": "FAC001"})

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert "opportunities" in result["data"]
    assert len(result["data"]["opportunities"]) > 0
    print("✓ energy_identify_efficiency_opportunities test passed")


def test_energy_recommend_optimizations():
    """Test recommendation generation tool."""
    from tools.energy_recommend_optimizations import execute

    result = execute({"facility_id": "FAC001"})

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert "recommendations" in result["data"]
    assert "disclaimer" in result["data"]
    print("✓ energy_recommend_optimizations test passed")


def test_energy_calculate_carbon_footprint():
    """Test carbon footprint calculation tool."""
    from tools.energy_calculate_carbon_footprint import execute

    result = execute({
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-30"
    })

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert result["data"]["total_emissions_kgco2"] > 0
    assert "breakdown" in result["data"]
    print("✓ energy_calculate_carbon_footprint test passed")


def test_energy_suggest_renewables():
    """Test renewable energy suggestion tool."""
    from tools.energy_suggest_renewables import execute

    result = execute({
        "facility_id": "FAC001",
        "renewable_types": ["solar"]
    })

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert "solar" in result["data"]["assessments"]
    assert "recommendation" in result["data"]
    print("✓ energy_suggest_renewables test passed")


def test_energy_estimate_savings():
    """Test savings estimation tool."""
    from tools.energy_estimate_savings import execute

    result = execute({
        "facility_id": "FAC001",
        "measures": [
            {"measure_type": "hvac", "efficiency_improvement": 15}
        ]
    })

    assert result["status"] == "success", f"Tool failed: {result.get('error')}"
    assert len(result["data"]["measure_analyses"]) == 1
    assert result["data"]["measure_analyses"][0]["annual_savings_kwh"] > 0
    print("✓ energy_estimate_savings test passed")


def test_skill_handlers():
    """Test skill handler routing."""
    from skills.energy_analysis.handler import run as energy_analysis_run
    from skills.efficiency_optimization.handler import run as efficiency_run
    from skills.renewable_integration.handler import run as renewable_run

    # Test energy_analysis skill
    result = energy_analysis_run("analyze_consumption", {
        "facility_id": "FAC001",
        "start_date": "2026-09-01",
        "end_date": "2026-09-07"
    })
    assert result["status"] == "success"
    print("✓ energy_analysis skill handler test passed")

    # Test unknown intent
    result = energy_analysis_run("unknown_intent", {})
    assert result["status"] == "error"
    assert "Unknown operation" in result["error"]
    print("✓ skill handler unknown intent test passed")


def test_data_store():
    """Test DataStore operations."""
    from apis.data_store import DataStore

    data_store = DataStore(data_dir=project_root / "data")

    # Test load operations
    facilities = data_store.load_facilities()
    assert len(facilities) > 0, "No facilities loaded"

    equipment = data_store.load_equipment()
    assert len(equipment) > 0, "No equipment loaded"

    measures = data_store.load_efficiency_measures()
    assert len(measures) > 0, "No efficiency measures loaded"

    print("✓ data_store test passed")


if __name__ == "__main__":
    print("\nRunning Energy Management Assistant Tests")
    print("=" * 50)

    test_data_files_exist()
    test_data_store()
    test_energy_analyze_consumption()
    test_energy_identify_efficiency_opportunities()
    test_energy_recommend_optimizations()
    test_energy_calculate_carbon_footprint()
    test_energy_suggest_renewables()
    test_energy_estimate_savings()
    test_skill_handlers()

    print("\n" + "=" * 50)
    print("✅ All tests passed!")