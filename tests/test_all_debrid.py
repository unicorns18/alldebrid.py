#pylint: disable=C0301
"""
Tests for the AllDebrid class.
"""
import os
import sys
import pytest
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid # pylint: disable=C0413

load_dotenv()

apikey = os.getenv("ALLDEBRID_API_KEY")
if not apikey:
    raise ValueError("API key not found in .env file")

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
        alldebrid = AllDebrid(apikey=apikey)

        # Act
        response = alldebrid.ping()

        # Assert
        assert response.get("status") == "success"

    # Tests that an invalid API key raises a ValueError.
    def test_invalid_api_key(self):
        """
        Ye shall test that an invalid API key raises a ValueError, me hearties!
        """
        # Arrange
        alldebrid = AllDebrid(apikey="invalid_api_key")

        # Act & Assert
        with pytest.raises(ValueError):
            alldebrid.user()

    def test_user_endpoint_without_api_key(self):
        """
        Avast ye, me mateys! Let's test the user endpoint without an API key. Shiver me timbers! The test should raise a ValueError.
        """
        alldebrid = AllDebrid(apikey=None)
        with pytest.raises(ValueError):
            alldebrid.user()

    def test_upload_file_empty_input(self):
        """
        Ahoy matey! This test checks if the upload_file method of our scurvy AllDebrid API raises an error when an empty input is given.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(files="")

    def test_invalid_endpoint_name(self):
        """
        Arrr! Ye scurvy dog! Test that when a name that be not on the list of valid endpoints is passed to the _request method, it raises an error, yarrr!
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid._request(method="GET", endpoint="invalid_endpoint")

    def test_missing_endpoint(self):
        """
        Arrr! Test that ye get an error when ye try to request a method with no endpoint, me matey!
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid._request(method="GET", endpoint="invalid_endpoint")

    # Tests that the ping method returns a valid response from the API.
    def test_ping(self):
        """
        Arrr, me hearties! Hoist the mainsail and let's test that the ping method be working! This here test should check that the ping method gives us a valid response from the API.
        """
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.ping()
        assert response.get("status") == "success"

    # Tests that the user method with a valid API key returns a valid response from the API.
    def test_user_valid_apikey(self):
        """
        Ahoy matey! We're testin' the user method with a valid API key to make sure we're gettin' a proper response from the API. Set sail and let's make it happen!
        """
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.user()
        assert response.get("status") == "success"

    # Tests that calling the user method without an API key raises a ValueError.
    def test_user_no_apikey(self):
        """
        Aye, matey! This test be checkin' if callin' the user method without an API key raises a ValueError.
        """
        alldebrid = AllDebrid(apikey=None)
        with pytest.raises(ValueError):
            alldebrid.user()

    # Tests that the download_link method with a valid link returns a valid response from the API.
    def test_download_link_valid_link(self):
        """
        Avast! Test that the download_link method with a valid link returns a valid response from the API.
        """
        pytest.skip("Skipping test_download_link_valid_link")
        # ad = AllDebrid(apikey=apikey)
        # response = ad.download_link(links="https://uptobox.com/8oht71xn63jb")
        # assert response.get("status") == "success"

    # Tests that calling the upload_file method without any files raises a ValueError.
    def test_upload_file_endpoint_without_files(self):
        """
        Arrr! Shiver me timbers, mateys! This test checks whether the upload_file endpoint raises a proper ValueError when called without any files.
        """
        alldebrid = AllDebrid(apikey="valid_api_key")
        with pytest.raises(ValueError):
            alldebrid.upload_file(files=None)

    def test_upload_file_endpoint_with_files(self):
        """
        Ahoy, ye scallywags! We be testing the upload_file method with files.
        """
        # TODO: Find a way to bypass the NO_SERVER error. (Proxies...?)
        pytest.skip("Skipping test_upload_file_endpoint_with_files")
        # if not os.path.exists("test_file.txt"):
        #     with open("test_file.txt", "w") as f:
        #         f.write("This is a test file.")
        #         f.close()

        # ad = AllDebrid(apikey=apikey)
        # response = ad.upload_file(files="test_file.txt")
        # assert response.get("status") == "success"

    def test_upload_file_endpoint_with_invalid_files(self):
        """
        Test that calling the upload_file method with invalid files raises a ValueError.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(files="invalid_file.txt")

    def test_upload_file_endpoint_with_no_file(self):
        """
        Arrr, me hearty! Test ye this code that tests the upload_file method with invalid files. It be like firing a cannon at an enemy ship and finding out that the powder be wet! We test that when ye provide an invalid file, the method raises a ValueError.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(files="")

    # TODO: Write the test for the upload_file method with multiple files.
    def test_upload_file_endpoint_with_multiple_files(self):
        """
        Arrrr, shiver me timbers! Ye be lookin' at the test that checks if the upload_file method can handle multiple files. But alas, we be unable to run this test due to a pesky NO_SERVER error. So let us pass on by and continue with our journey.
        """
        # TODO: Find a way to bypass the NO_SERVER error. (Proxies...?)

    def test_magnet_upload_endpoint_with_valid_magnet_link(self):
        """
        Ahoy, matey! Avast ye, this test be testing the magnet_upload method! We'll be checkin' that the method gives us a jolly roger of a response from the API when we pass it a valid magnet link. Let's set sail and hoist the colors!
        """
        pytest.skip("Skipping test_magnet_upload_endpoint_with_valid_magnet_link")
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.upload_magnets(magnets="magnet:?xt=urn:btih:C3DA9A3DC2CE14D0D4FC0E87D1B2023502F8DCD6&dn=The+Shawshank+Redemption+%281994%29+%5B2160p%5D+%5BYTS.MX%5D&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2970%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=https%3A%2F%2Fopentracker.i2p.rocks%3A443%2Fannounce")
        assert response.get("status") == "success"

    def test_get_magnet_info(self):
        """
        Shiver me timbers!
        Test that callin' the get_magnet_info method with a valid magnet link returns a valid,
        response from the API.
        """
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.get_magnet_status(magnet_id=186284422)
        assert response.get("status") == "success"