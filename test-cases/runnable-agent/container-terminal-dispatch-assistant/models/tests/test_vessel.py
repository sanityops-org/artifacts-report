"""
Ship and berth model test

Test the verification logic of Vessel and Berth Pydantic models.
"""

import pytest
from pydantic import ValidationError
from models.vessel import Vessel, Berth
from models.enums import VesselStatus, BerthStatus


class TestVesselModel:
    """Vessel Model test class"""

    def test_vessel_model_creation(self):
        """Test the normal creation of the ship model"""
        vessel = Vessel(
            vessel_id="V001",
            vessel_name="Pacific Star",
            vessel_type="container_ship",
            length=300.5,
            draft=12.5,
            eta="2024-01-15T08:00:00",
            container_count=5000,
            inbound_containers=2500,
            outbound_containers=2500,
        )

        assert vessel.vessel_id == "V001"
        assert vessel.vessel_name == "Pacific Star"
        assert vessel.vessel_type == "container_ship"
        assert vessel.length == 300.5
        assert vessel.draft == 12.5
        assert vessel.eta == "2024-01-15T08:00:00"
        assert vessel.etd is None
        assert vessel.status == VesselStatus.INBOUND
        assert vessel.assigned_berth is None
        assert vessel.container_count == 5000
        assert vessel.inbound_containers == 2500
        assert vessel.outbound_containers == 2500

    def test_vessel_id_pattern_validation(self):
        r"""Test ship ID format verification (must match ^V\d{3}$)"""
        # Valid format
        valid_ids = ["V001", "V123", "V999"]
        for vid in valid_ids:
            vessel = Vessel(
                vessel_id=vid,
                vessel_name="Test ship",
                length=200,
                draft=10,
                eta="2024-01-15T08:00:00",
                container_count=1000,
                inbound_containers=500,
                outbound_containers=500,
            )
            assert vessel.vessel_id == vid

        # Invalid format
        invalid_ids = ["v001", "V01", "V0001", "V1A2", "X001", "V00", ""]
        for vid in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                Vessel(
                    vessel_id=vid,
                    vessel_name="Test ship",
                    length=200,
                    draft=10,
                    eta="2024-01-15T08:00:00",
                    container_count=1000,
                    inbound_containers=500,
                    outbound_containers=500,
                )
            # The verification error contains the vessel_id field
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("vessel_id",) for e in errors)

    def test_vessel_length_range_validation(self):
        """Test ship length range verification (0 < length <= 400)"""
        # Effective length
        valid_lengths = [1.0, 100.5, 399.9, 400.0]
        for length in valid_lengths:
            vessel = Vessel(
                vessel_id="V001",
                vessel_name="Test ship",
                length=length,
                draft=10,
                eta="2024-01-15T08:00:00",
                container_count=1000,
                inbound_containers=500,
                outbound_containers=500,
            )
            assert vessel.length == length

        # Invalid length: 0, negative, more than400
        invalid_lengths = [0, -10, 400.1, 500]
        for length in invalid_lengths:
            with pytest.raises(ValidationError) as exc_info:
                Vessel(
                    vessel_id="V001",
                    vessel_name="Test ship",
                    length=length,
                    draft=10,
                    eta="2024-01-15T08:00:00",
                    container_count=1000,
                    inbound_containers=500,
                    outbound_containers=500,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("length",) for e in errors)

    def test_vessel_draft_range_validation(self):
        """Test the ship's tain range verification (0 < draft <= 20)"""
        # Effective water
        valid_drafts = [0.1, 10.0, 19.9, 20.0]
        for draft in valid_drafts:
            vessel = Vessel(
                vessel_id="V001",
                vessel_name="Test ship",
                length=200,
                draft=draft,
                eta="2024-01-15T08:00:00",
                container_count=1000,
                inbound_containers=500,
                outbound_containers=500,
            )
            assert vessel.draft == draft

        # Invalid water
        invalid_drafts = [0, -5, 20.1, 25]
        for draft in invalid_drafts:
            with pytest.raises(ValidationError) as exc_info:
                Vessel(
                    vessel_id="V001",
                    vessel_name="Test ship",
                    length=200,
                    draft=draft,
                    eta="2024-01-15T08:00:00",
                    container_count=1000,
                    inbound_containers=500,
                    outbound_containers=500,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("draft",) for e in errors)

    def test_vessel_name_validation(self):
        """Test ship name verification (min_length=2, max_length=50)"""
        # Valid name
        valid_names = ["AB", "Pacific Star", "A" * 50]
        for name in valid_names:
            vessel = Vessel(
                vessel_id="V001",
                vessel_name=name,
                length=200,
                draft=10,
                eta="2024-01-15T08:00:00",
                container_count=1000,
                inbound_containers=500,
                outbound_containers=500,
            )
            assert vessel.vessel_name == name

        # Invalid name: insufficient length or over-length
        invalid_names = ["A", "", "A" * 51]
        for name in invalid_names:
            with pytest.raises(ValidationError) as exc_info:
                Vessel(
                    vessel_id="V001",
                    vessel_name=name,
                    length=200,
                    draft=10,
                    eta="2024-01-15T08:00:00",
                    container_count=1000,
                    inbound_containers=500,
                    outbound_containers=500,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("vessel_name",) for e in errors)

    def test_vessel_container_count_validation(self):
        """Test container quantity verification (ge=0)"""
        # Effective quantity
        valid_counts = [0, 100, 5000]
        for count in valid_counts:
            vessel = Vessel(
                vessel_id="V001",
                vessel_name="Test ship",
                length=200,
                draft=10,
                eta="2024-01-15T08:00:00",
                container_count=count,
                inbound_containers=500,
                outbound_containers=500,
            )
            assert vessel.container_count == count

        # Invalid quantity
        with pytest.raises(ValidationError) as exc_info:
            Vessel(
                vessel_id="V001",
                vessel_name="Test ship",
                length=200,
                draft=10,
                eta="2024-01-15T08:00:00",
                container_count=-1,
                inbound_containers=500,
                outbound_containers=500,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("container_count",) for e in errors)

    def test_vessel_default_values(self):
        """Test the default value of the ship"""
        vessel = Vessel(
            vessel_id="V001",
            vessel_name="Test ship",
            length=200,
            draft=10,
            eta="2024-01-15T08:00:00",
            container_count=1000,
            inbound_containers=500,
            outbound_containers=500,
        )
        assert vessel.vessel_type == "container_ship"
        assert vessel.status == VesselStatus.INBOUND
        assert vessel.etd is None
        assert vessel.assigned_berth is None


class TestBerthModel:
    """Berth Model test class"""

    def test_berth_model_creation(self):
        """Test the normal creation of the berth model"""
        berth = Berth(
            berth_id="B01",
            berth_name="No.1 berth",
            length=350.0,
            max_draft=16.0,
        )

        assert berth.berth_id == "B01"
        assert berth.berth_name == "No.1 berth"
        assert berth.length == 350.0
        assert berth.max_draft == 16.0
        assert berth.status == BerthStatus.AVAILABLE
        assert berth.current_vessel is None
        assert berth.available_from is None

    def test_berth_id_pattern_validation(self):
        r"""Test berth ID format verification (must match ^B\d{2}$)"""
        # Valid format
        valid_ids = ["B01", "B12", "B99"]
        for bid in valid_ids:
            berth = Berth(
                berth_id=bid,
                berth_name="Test berth",
                length=300,
                max_draft=15,
            )
            assert berth.berth_id == bid

        # Invalid format
        invalid_ids = ["b01", "B1", "B001", "B1A", "X01", "B0", ""]
        for bid in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                Berth(
                    berth_id=bid,
                    berth_name="Test berth",
                    length=300,
                    max_draft=15,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("berth_id",) for e in errors)

    def test_berth_length_validation(self):
        """Test the berth length verification (gt=0)"""
        # Effective length
        valid_lengths = [0.1, 100, 500]
        for length in valid_lengths:
            berth = Berth(
                berth_id="B01",
                berth_name="Test berth",
                length=length,
                max_draft=15,
            )
            assert berth.length == length

        # Invalid length
        invalid_lengths = [0, -10]
        for length in invalid_lengths:
            with pytest.raises(ValidationError) as exc_info:
                Berth(
                    berth_id="B01",
                    berth_name="Test berth",
                    length=length,
                    max_draft=15,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("length",) for e in errors)

    def test_berth_max_draft_validation(self):
        """Test the maximum talk verification of the berth (gt=0)"""
        # Effective water
        valid_drafts = [0.1, 10, 20]
        for draft in valid_drafts:
            berth = Berth(
                berth_id="B01",
                berth_name="Test berth",
                length=300,
                max_draft=draft,
            )
            assert berth.max_draft == draft

        # Invalid water
        invalid_drafts = [0, -5]
        for draft in invalid_drafts:
            with pytest.raises(ValidationError) as exc_info:
                Berth(
                    berth_id="B01",
                    berth_name="Test berth",
                    length=300,
                    max_draft=draft,
                )
            errors = exc_info.value.errors()
            assert any(e["loc"] == ("max_draft",) for e in errors)

    def test_berth_default_values(self):
        """Test the default value of the berth"""
        berth = Berth(
            berth_id="B01",
            berth_name="Test berth",
            length=300,
            max_draft=15,
        )
        assert berth.status == BerthStatus.AVAILABLE
        assert berth.current_vessel is None
        assert berth.available_from is None

    def test_berth_with_assigned_vessel(self):
        """Test the berth with ships docked"""
        berth = Berth(
            berth_id="B01",
            berth_name="No.1 berth",
            length=350.0,
            max_draft=16.0,
            status=BerthStatus.OCCUPIED,
            current_vessel="V001",
            available_from="2024-01-15T18:00:00",
        )

        assert berth.status == BerthStatus.OCCUPIED
        assert berth.current_vessel == "V001"
        assert berth.available_from == "2024-01-15T18:00:00"
