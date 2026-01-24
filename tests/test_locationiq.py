import pytest
import requests
from unittest.mock import Mock, patch
from app.services.locationiq import get_coordinates, LOCATIONIQ_PATH

def test_get_coordinates_success():
    # Arrange
    mock_response_data = [
        {
            "lat": "37.7749",
            "lon": "-122.4194"
        }
    ]

    with patch("app.services.locationiq.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response_data
        mock_get.return_value.raise_for_status.return_value = None

        data = {
            "address_line1": "1 Market St",
            "address_line2": "",
            "city": "San Francisco",
            "state": "CA",
            "postal_code": "94105"
        }
        # Act
        coords = get_coordinates(data)

        # Assert
        assert coords == {"latitude": 37.7749, "longitude": -122.4194}

def test_get_coordinates_address_not_found():
    # Arrange
    data = {
        "address_line1": "Unknown Address",
        "address_line2": "",
        "city": "Nowhere",
        "state": "ZZ",
        "postal_code": "00000"
    }

    fake_response_data = Mock()
    fake_response_data.json.return_value = []
    fake_response_data.raise_for_status.return_value = None

    with patch("app.services.locationiq.requests.get", return_value=fake_response_data):
        # Act & Assert
        with pytest.raises(ValueError, match="Address not found"):
            get_coordinates(data)
