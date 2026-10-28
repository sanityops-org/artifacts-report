# TOSAnalog interface test
"""Test the TOS login and permission management functions"""

import uuid
import pytest
from apis import tos_api


class TestTosApiLogin:
    """Login function test"""

    def test_login_berth_scheduler(self):
        """Verify the login and permissions of the parking dispatcher"""
        result = tos_api.login("Parking dispatcher")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Parking dispatcher"
        assert data["permissions"] == ["berth_scheduling"]
        assert data["can_issue_commands"] is True
        assert "session_id" in data
        assert uuid.UUID(data["session_id"])  # The verification is valid.UUID

    def test_login_supervisor(self):
        """Verify that the operation supervisor has all 4 domain permissions."""
        result = tos_api.login("Operation supervisor")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Operation supervisor"
        assert set(data["permissions"]) == {
            "berth_scheduling",
            "yard_scheduling",
            "equipment_scheduling",
            "gate_scheduling"
        }
        assert data["can_issue_commands"] is True

    def test_login_manager(self):
        """VERIFICATION CODE HEAD MANAGER can_issue_commands=False"""
        result = tos_api.login("Dock manager")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Dock manager"
        assert set(data["permissions"]) == {
            "berth_scheduling",
            "yard_scheduling",
            "equipment_scheduling",
            "gate_scheduling"
        }
        assert data["can_issue_commands"] is False

    def test_login_unknown_role(self):
        """Unknown role login returnerror"""
        result = tos_api.login("Unknown role")

        assert result["status"] == "error"
        assert "error" in result
        assert "Unknown role" in result["error"] or "non-existent" in result["error"]

    def test_login_yard_scheduler(self):
        """Verify the login of the warehouse dispatcher"""
        result = tos_api.login("Stacking dispatcher")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Stacking dispatcher"
        assert data["permissions"] == ["yard_scheduling"]
        assert data["can_issue_commands"] is True

    def test_login_equipment_scheduler(self):
        """Verify the login of the device dispatcher"""
        result = tos_api.login("Equipment dispatcher")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Equipment dispatcher"
        assert data["permissions"] == ["equipment_scheduling"]
        assert data["can_issue_commands"] is True

    def test_login_gate_scheduler(self):
        """Verify the login of the gate dispatcher"""
        result = tos_api.login("Gate dispatcher")

        assert result["status"] == "success"
        data = result["data"]
        assert data["role"] == "Gate dispatcher"
        assert data["permissions"] == ["gate_scheduling"]
        assert data["can_issue_commands"] is True


class TestTosApiPermission:
    """Permission verification test"""

    def test_check_permission(self):
        """The berth dispatcher has permission for berth_scheduling, but not for yard_scheduling."""
        # Log in to the parking dispatcher
        result = tos_api.login("Parking dispatcher")
        session_id = result["data"]["session_id"]

        # Verification permission
        assert tos_api.check_permission(session_id, "berth_scheduling") is True
        assert tos_api.check_permission(session_id, "yard_scheduling") is False

    def test_check_permission_supervisor(self):
        """Supervisors have authority in all fields."""
        result = tos_api.login("Operation supervisor")
        session_id = result["data"]["session_id"]

        assert tos_api.check_permission(session_id, "berth_scheduling") is True
        assert tos_api.check_permission(session_id, "yard_scheduling") is True
        assert tos_api.check_permission(session_id, "equipment_scheduling") is True
        assert tos_api.check_permission(session_id, "gate_scheduling") is True

    def test_check_permission_invalid_session(self):
        """Invalid session returnFalse"""
        assert tos_api.check_permission("invalid-session-id", "berth_scheduling") is False

    def test_can_issue_commands(self):
        """Verify the command permission"""
        # The berth dispatcher can issue instructions.
        result = tos_api.login("Parking dispatcher")
        session_id = result["data"]["session_id"]
        assert tos_api.can_issue_commands(session_id) is True

        # The dock manager cannot issue instructions.
        result = tos_api.login("Dock manager")
        session_id = result["data"]["session_id"]
        assert tos_api.can_issue_commands(session_id) is False

    def test_can_issue_commands_invalid_session(self):
        """Invalid session returnFalse"""
        assert tos_api.can_issue_commands("invalid-session-id") is False


class TestTosApiSession:
    """Session management test"""

    def test_get_session(self):
        """Get the conversation information"""
        result = tos_api.login("Parking dispatcher")
        session_id = result["data"]["session_id"]

        session = tos_api.get_session(session_id)
        assert session is not None
        assert session["role"] == "Parking dispatcher"

    def test_get_session_invalid(self):
        """Get invalid session returnNone"""
        assert tos_api.get_session("invalid-session-id") is None

    def test_logout(self):
        """Log out function"""
        result = tos_api.login("Parking dispatcher")
        session_id = result["data"]["session_id"]

        # Confirm the existence of the session
        assert tos_api.get_session(session_id) is not None

        # Log out
        logout_result = tos_api.logout(session_id)
        assert logout_result["status"] == "success"

        # Confirm that the session has been deleted
        assert tos_api.get_session(session_id) is None

    def test_logout_invalid_session(self):
        """Log out of invalid session"""
        result = tos_api.logout("invalid-session-id")
        assert result["status"] == "error"
