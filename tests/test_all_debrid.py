import os
import pytest 
import sys
from dotenv import load_dotenv
sys.path.append("..")
from alldebrid import AllDebrid, AllDebridError, endpoints, HOST

load_dotenv(dotenv_path="../.env", verbose=True)

apikey = os.getenv("ALLDEBRID_API_KEY")

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
        ad = AllDebrid(apikey=apikey)

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
        ad = AllDebrid(apikey="invalid_api_key")

        # Act & Assert
        with pytest.raises(ValueError):
            ad.user()

    def test_successful_ping_request(self):
        """
        Tests that a successful request is made to the ping endpoint.
        """
        ad = AllDebrid(apikey=apikey)
        endpoint = endpoints.get("ping")
        response_json = {"status": "success", "data": {"ping": "pong"}}
        response = ad._request(method="GET", endpoint=endpoint)
        assert response == response_json

    def test_upload_file_empty_input(self):
        """
        Tests that an error is raised when an empty input is provided to the upload_file method.
        """
        ad = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            ad.upload_file(files="")

    def test_invalid_endpoint_name(self):
        """
        Tests that an error is raised when an invalid endpoint name is provided to the _request method.
        """
        ad = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            ad._request(method="GET", endpoint="invalid_endpoint")

    def test_missing_endpoint(self):
        """
        Tests that an error is raised when an endpoint is not found for a given method.
        """
        ad = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            ad._request(method="GET", endpoint="invalid_endpoint")

    # Tests that the ping method returns a valid response from the API. 
    def test_ping(self):
        """
        Test that the ping method returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.ping()
        assert response.get("status") == "success"

    # Tests that the user method with a valid API key returns a valid response from the API. 
    def test_user_valid_apikey(self):
        """
        Test that the user method with a valid API key returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.user()
        assert response.get("status") == "success"

    # Tests that calling the user method without an API key raises a ValueError. 
    def test_user_no_apikey(self):
        """
        Test that calling the user method without an API key raises a ValueError.
        """
        ad = AllDebrid(apikey=None)
        with pytest.raises(ValueError):
            ad.user()

    # Tests that the download_link method with a valid link returns a valid response from the API. 
    def test_download_link_valid_link(self):
        """
        Test that the download_link method with a valid link returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.download_link(links="https://uptobox.com/8oht71xn63jb")
        assert response.get("status") == "success"
