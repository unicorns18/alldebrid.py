import os
import pytest 
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid, AllDebridError, endpoints, HOST

load_dotenv(dotenv_path="../.env.sample", verbose=True)

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
    
    def test_user_endpoint_without_api_key(self):
        """
        Test that calling the user method without an API key raises a ValueError.
        """
        ad = AllDebrid(apikey=None)
        with pytest.raises(ValueError):
            ad.user()

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
    
    # Tests that calling the upload_file method without any files raises a ValueError. 
    def test_upload_file_endpoint_without_files(self):
        """
        Test that calling the upload_file method without any files raises a ValueError.
        """
        ad = AllDebrid(apikey="valid_api_key")
        with pytest.raises(ValueError):
            ad.upload_file(files=None)

    def test_upload_file_endpoint_with_files(self):
        """
        Test that calling the upload_file method with files returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.upload_file(files="test_file.txt")
        assert response.get("status") == "success"

    def test_upload_file_endpoint_with_invalid_files(self):
        """
        Test that calling the upload_file method with invalid files raises a ValueError.
        """
        ad = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            ad.upload_file(files="invalid_file.txt")

    def test_upload_file_endpoint_with_no_file(self):
        """
        Test that calling the upload_file method with no file raises a ValueError.
        """
        ad = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            ad.upload_file(files="")

    # TODO: Write the test for the upload_file method with multiple files.
    # def test_upload_file_endpoint_with_multiple_files(self):
    #     pass

    def test_magnet_upload_endpoint_with_valid_magnet_link(self):
        """
        Test that calling the magnet_upload method with a valid magnet link returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.upload_magnets(magnets="magnet:?xt=urn:btih:C3DA9A3DC2CE14D0D4FC0E87D1B2023502F8DCD6&dn=The+Shawshank+Redemption+%281994%29+%5B2160p%5D+%5BYTS.MX%5D&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2970%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=https%3A%2F%2Fopentracker.i2p.rocks%3A443%2Fannounce")
        assert response.get("status") == "success"

    def test_get_magnet_info(self):
        """
        Test that calling the get_magnet_info method with a valid magnet link returns a valid response from the API.
        """
        ad = AllDebrid(apikey=apikey)
        response = ad.get_magnet_status(magnet_id=186284422)
        assert response.get("status") == "success"
