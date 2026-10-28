"""
Stacking field model test module

Test the creation, verification and behavior of YardBlock and Container models.
"""

import pytest
from pydantic import ValidationError

from models.enums import BlockStatus, ContainerType, ContainerSize
from models.yard import YardBlock, Container


class TestYardBlock:
    """YardBlock Model test"""

    def test_yard_block_creation(self):
        """Test the normal creation of the stack block"""
        block = YardBlock(
            block_id="A01",
            block_name="ADistrict No. 1 storage field",
            type=ContainerType.IMPORT,
            capacity=1500,
        )

        assert block.block_id == "A01"
        assert block.block_name == "ADistrict No. 1 storage field"
        assert block.type == ContainerType.IMPORT
        assert block.capacity == 1500
        assert block.occupied == 0  # Default value
        assert block.tiers_max == 5  # Default value
        assert block.status == BlockStatus.OPERATIONAL  # Default value

    def test_yard_block_capacity_validation(self):
        """Test the block capacity verification of the warehouse"""
        # The capacity must be greater than0
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=0,  # Invalid: the capacity is0
            )
        assert "greater than 0" in str(exc_info.value)

        # The capacity cannot exceed2000
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=2500,  # Invalid: the capacity exceeds2000
            )
        assert "less than or equal to 2000" in str(exc_info.value)

    def test_yard_block_id_validation(self):
        """Test the stack block ID format verification"""
        # Invalid format: missing numbers
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
            )
        assert "block_id" in str(exc_info.value)

        # Invalid format: more than 2 digits
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A123",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
            )
        assert "block_id" in str(exc_info.value)

        # Invalid format: letters are not in the A-F range
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="G01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
            )

    def test_yard_block_tiers_validation(self):
        """Test the verification of the number of layers of the stack"""
        # The number of layers must be at least1
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
                tiers_max=0,  # Be invalid
            )
        assert "greater than or equal to 1" in str(exc_info.value)

        # The number of layers cannot exceed9
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
                tiers_max=10,  # Be invalid
            )
        assert "less than or equal to 9" in str(exc_info.value)

    def test_yard_block_occupied_validation(self):
        """Test the occupancy verification"""
        # It has been occupied and cannot be negative.
        with pytest.raises(ValidationError) as exc_info:
            YardBlock(
                block_id="A01",
                block_name="Test dump",
                type=ContainerType.EXPORT,
                capacity=1000,
                occupied=-1,  # Be invalid
            )
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_yard_block_valid_id_range(self):
        """Test the range of valid storage block ID"""
        # Test all valid letter ranges A-F
        for letter in "ABCDEF":
            block = YardBlock(
                block_id=f"{letter}01",
                block_name=f"{letter}District No. 1 storage field",
                type=ContainerType.IMPORT,
                capacity=1000,
            )
            assert block.block_id == f"{letter}01"

        # Test the digital range 01-99
        block = YardBlock(
            block_id="A99",
            block_name="Test dump",
            type=ContainerType.EXPORT,
            capacity=1000,
        )
        assert block.block_id == "A99"


class TestContainer:
    """Container Model test"""

    def test_container_creation(self):
        """Test the normal creation of the container"""
        container = Container(
            container_id="MSCU1234567",
            size=ContainerSize.FORTY_GP,
            type=ContainerType.IMPORT,
            weight=25.5,
        )

        assert container.container_id == "MSCU1234567"
        assert container.size == ContainerSize.FORTY_GP
        assert container.type == ContainerType.IMPORT
        assert container.weight == 25.5
        assert container.vessel_id is None  # Default value
        assert container.block_id is None  # Default value
        assert container.bay is None  # Default value
        assert container.row is None  # Default value
        assert container.tier is None  # Default value

    def test_container_id_iso6346_validation(self):
        """Test container ID ISO 6346 format verification"""
        # Invalid format: the number bit is less than 7 digits
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU123456",  # Only 6 digits
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
            )
        assert "container_id" in str(exc_info.value)

        # Invalid format: the owner code contains non-alphabets
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MS11234567",  # The 4th digit is a number, which should be a letter.
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
            )
        assert "container_id" in str(exc_info.value)

        # Invalid format: the length is wrong
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU12345678",  # 12Bit, should be 11 bits
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
            )
        assert "container_id" in str(exc_info.value)

    def test_container_weight_validation(self):
        """Test container weight verification"""
        # The weight cannot be negative.
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=-1.0,  # Be invalid
            )
        assert "greater than or equal to 0" in str(exc_info.value)

        # The weight should not exceed 40 tons.
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=45.0,  # Be invalid
            )
        assert "less than or equal to 40" in str(exc_info.value)

    def test_container_position_validation(self):
        """Test container location field verification"""
        # Valid location information
        container = Container(
            container_id="MSCU1234567",
            size=ContainerSize.FORTY_GP,
            type=ContainerType.IMPORT,
            weight=20.0,
            vessel_id="V001",
            block_id="A01",
            bay=10,
            row=6,
            tier=4,
        )
        assert container.bay == 10
        assert container.row == 6
        assert container.tier == 4

        # bay Must >= 1
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
                bay=0,  # Be invalid
            )
        assert "greater than or equal to 1" in str(exc_info.value)

        # row Must >= 1
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
                row=0,  # Be invalid
            )
        assert "greater than or equal to 1" in str(exc_info.value)

        # tier Must >= 1 and <= 9
        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
                tier=0,  # Be invalid
            )
        assert "greater than or equal to 1" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            Container(
                container_id="MSCU1234567",
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.EXPORT,
                weight=10.0,
                tier=10,  # Be invalid
            )
        assert "less than or equal to 9" in str(exc_info.value)

    def test_container_valid_iso6346_ids(self):
        """Test the effective ISO 6346 format containerID"""
        valid_ids = [
            "MSCU1234567",
            "CMAU9876543",
            "HLXU5551234",
            "YMLU0000001",
            "EGLV9999999",
        ]

        for container_id in valid_ids:
            container = Container(
                container_id=container_id,
                size=ContainerSize.TWENTY_GP,
                type=ContainerType.IMPORT,
                weight=15.0,
            )
            assert container.container_id == container_id

    def test_container_with_all_optional_fields(self):
        """Test container creation with all optional fields"""
        container = Container(
            container_id="MSCU1234567",
            size=ContainerSize.FORTY_HQ,
            type=ContainerType.DANGEROUS,
            weight=30.0,
            vessel_id="V005",
            block_id="C03",
            bay=15,
            row=3,
            tier=2,
        )

        assert container.container_id == "MSCU1234567"
        assert container.size == ContainerSize.FORTY_HQ
        assert container.type == ContainerType.DANGEROUS
        assert container.weight == 30.0
        assert container.vessel_id == "V005"
        assert container.block_id == "C03"
        assert container.bay == 15
        assert container.row == 3
        assert container.tier == 2
