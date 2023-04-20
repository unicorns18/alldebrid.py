import pytest, sys
sys.path.append("..")
from alldebrid import AllDebrid, AllDebridError

class TestAllDebrid:
    """
    Tests for the AllDebrid class.
    """

    # Tests that the ping endpoint returns a successful response. 
    def test_ping_success(self):
        """
        Ye shall test that the ping endpoint returns a successful response, me hearties!
        """
        # Arrange
        apikey = "valid_api_key"
        ad = AllDebrid(apikey)

        # Act
        response = ad.ping()

        # Assert
        assert response.get("status") == "success"

    # Tests that an invalid API key raises a ValueError. 
    def test_invalid_api_key(self):
        """
        Ye shall test that an invalid API key raises a ValueError, me hearties!
        """
        # Arrange
        apikey = ""
        ad = AllDebrid(apikey=apikey)

        # Act & Assert
        with pytest.raises(ValueError):
            ad.user()