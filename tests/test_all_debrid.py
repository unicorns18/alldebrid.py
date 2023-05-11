#pylint: disable=C0301
"""
Tests for the AllDebrid class.
"""
import os
import sys
import pytest
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid # pylint: disable=C0413

load_dotenv()

apikey = os.getenv("ALLDEBRID_API_KEY")
if not apikey:
    raise ValueError("API key not found in .env file")

class TestAllDebrid:
    """
    Tests for the AllDebrid class.
    """
    # Tests that an invalid API key raises a ValueError.
    def test_invalid_api_key(self):
        """
        Ye shall test that an invalid API key raises a ValueError, me hearties!
        """
        # Arrange
        alldebrid = AllDebrid(apikey="invalid_api_key")

        # Assert
        with pytest.raises(ValueError):
            alldebrid.ping()

    # TODO: Re-implementing all the tests in an organized order soon enough...
    