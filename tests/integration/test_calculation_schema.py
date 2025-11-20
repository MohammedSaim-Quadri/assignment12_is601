import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse
)

def test_calculation_create_valid():
    """Test creating a valid CalculationCreate schema."""
    data = {
        "type": "addition",
        "inputs": [10.5, 3.0],
        "user_id": uuid4()
    }
    calc = CalculationCreate(**data)
    assert calc.type == "addition"
    assert calc.inputs == [10.5, 3.0]
    assert calc.user_id is not None

def test_calculation_create_missing_type():
    """Test CalculationCreate fails if 'type' is missing."""
    data = {
        "inputs": [10.5, 3.0],
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "required" in str(exc_info.value).lower()

def test_calculation_create_missing_inputs():
    """Test CalculationCreate fails if 'inputs' is missing."""
    data = {
        "type": "multiplication",
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    assert "required" in str(exc_info.value).lower()

def test_calculation_create_invalid_inputs():
    """Test CalculationCreate fails if 'inputs' is not a list of floats."""
    data = {
        "type": "division",
        "inputs": "not-a-list",
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    error_message = str(exc_info.value)
    # Ensure that our custom error message is present (case-insensitive)
    assert "input should be a valid list" in error_message.lower(), error_message

def test_calculation_create_unsupported_type():
    """Test CalculationCreate fails if an unsupported calculation type is provided."""
    data = {
        "type": "square_root",  # Unsupported type
        "inputs": [25],
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    error_message = str(exc_info.value).lower()
    # Check that the error message indicates the value is not permitted.
    assert "one of" in error_message or "not a valid" in error_message

def test_calculation_update_valid():
    """Test a valid partial update with CalculationUpdate."""
    data = {
        "inputs": [42.0, 7.0]
    }
    calc_update = CalculationUpdate(**data)
    assert calc_update.inputs == [42.0, 7.0]

def test_calculation_update_no_fields():
    """Test that an empty update is allowed (i.e., no fields)."""
    calc_update = CalculationUpdate()
    assert calc_update.inputs is None

def test_calculation_response_valid():
    """Test creating a valid CalculationResponse schema."""
    data = {
        "id": uuid4(),
        "user_id": uuid4(),
        "type": "subtraction",
        "inputs": [20, 5],
        "result": 15.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    calc_response = CalculationResponse(**data)
    assert calc_response.id is not None
    assert calc_response.user_id is not None
    assert calc_response.type == "subtraction"
    assert calc_response.inputs == [20, 5]
    assert calc_response.result == 15.5


# ============================================================================
# NEW TESTS: Type Update Functionality
# ============================================================================

def test_calculation_update_with_type_only():
    """Test CalculationUpdate accepts only type field."""
    data = {
        "type": "multiplication"
    }
    calc_update = CalculationUpdate(**data)
    assert calc_update.type == "multiplication"
    assert calc_update.inputs is None


def test_calculation_update_with_type_and_inputs():
    """Test CalculationUpdate accepts both type and inputs."""
    data = {
        "type": "division",
        "inputs": [100.0, 5.0, 2.0]
    }
    calc_update = CalculationUpdate(**data)
    assert calc_update.type == "division"
    assert calc_update.inputs == [100.0, 5.0, 2.0]


def test_calculation_update_valid_type_variations():
    """Test CalculationUpdate accepts all valid calculation types."""
    valid_types = ["addition", "subtraction", "multiplication", "division"]
    
    for calc_type in valid_types:
        data = {
            "type": calc_type,
            "inputs": [10, 5]
        }
        calc_update = CalculationUpdate(**data)
        assert calc_update.type == calc_type


def test_calculation_update_invalid_type():
    """Test CalculationUpdate rejects invalid calculation type."""
    data = {
        "type": "modulus",  # Invalid type
        "inputs": [10, 3]
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationUpdate(**data)
    error_message = str(exc_info.value).lower()
    assert "one of" in error_message or "type must be" in error_message


def test_calculation_update_type_case_insensitive():
    """Test CalculationUpdate handles type case insensitively."""
    data = {
        "type": "MULTIPLICATION",  # Uppercase
        "inputs": [5, 4]
    }
    calc_update = CalculationUpdate(**data)
    assert calc_update.type == "multiplication"  # Should be normalized to lowercase


def test_calculation_update_division_with_zero_inputs():
    """Test CalculationUpdate validates division by zero."""
    data = {
        "type": "division",
        "inputs": [100, 0]  # Division by zero
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationUpdate(**data)
    error_message = str(exc_info.value).lower()
    assert "divide by zero" in error_message or "cannot divide" in error_message