"""Tests for prompt contract compliance."""

import sys
from pathlib import Path
import pytest

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestPromptContract:
    """Verify system prompt contains required guardrails."""

    @pytest.fixture
    def system_prompt(self):
        prompt_path = project_root / "prompts" / "system.txt"
        return prompt_path.read_text(encoding="utf-8")

    def test_guardrail_1_no_booking(self, system_prompt):
        """Check guardrail 1: Cannot book shipments."""
        assert "Cannot Book Shipments" in system_prompt or "cannot book" in system_prompt.lower()
        assert "information assistant" in system_prompt.lower()

    def test_guardrail_2_no_payment(self, system_prompt):
        """Check guardrail 2: Cannot process payments."""
        assert "Cannot Process Payments" in system_prompt or "cannot process payment" in system_prompt.lower()
        assert "estimate" in system_prompt.lower()

    def test_guardrail_3_no_contract_modification(self, system_prompt):
        """Check guardrail 3: Cannot modify carrier contracts."""
        assert "Cannot Modify Carrier Contracts" in system_prompt or "cannot modify" in system_prompt.lower()

    def test_has_identity(self, system_prompt):
        """Check system prompt has identity section."""
        assert "Freight Logistics Assistant" in system_prompt
        assert "logistics" in system_prompt.lower()

    def test_has_tool_usage_guide(self, system_prompt):
        """Check system prompt has tool usage guide."""
        assert "Tool Usage" in system_prompt or "tool" in system_prompt.lower()
        assert "shipment_get_status" in system_prompt or "tracking_number" in system_prompt

    def test_has_output_standards(self, system_prompt):
        """Check system prompt has output standards."""
        assert "Output" in system_prompt or "response" in system_prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])