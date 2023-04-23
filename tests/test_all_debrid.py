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
        with pytest.raises(ValueError):
            alldebrid = AllDebrid(apikey="invalid_api_key")

    def test_upload_file_empty_input(self):
        """
        Ahoy matey! This test checks if the upload_file method of our scurvy AllDebrid API raises an error when an empty input is given.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(file_paths="")

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
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(file_paths=None)

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
            alldebrid.upload_file(file_paths="invalid_file.txt")

    def test_upload_file_endpoint_with_no_file(self):
        """
        Arrr, me hearty! Test ye this code that tests the upload_file method with invalid files. It be like firing a cannon at an enemy ship and finding out that the powder be wet! We test that when ye provide an invalid file, the method raises a ValueError.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.upload_file(file_paths="")

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
        # Returns a NO_SERVER error on Github Actions.
        pytest.skip("Skipping test_magnet_upload_endpoint_with_valid_magnet_link")

    def test_get_magnet_info(self):
        """
        Shiver me timbers!
        Test that callin' the get_magnet_info method with a valid magnet link returns a valid,
        response from the API.
        """
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.get_magnet_status(magnet_id=186284422)
        assert response.get("status") == "success"

    def test_get_pin(self):
        """
        Arrr! Hoist the Jolly Roger! Test that the get_pin method returns a valid response from the API, me hearties!
        """
        alldebrid = AllDebrid(apikey=apikey)
        response = alldebrid.get_pin()
        assert response.get("status") == "success"

    def test_get_direct_stream_link_returns_string(self):
        """
        Ye matey, this test be checkin' if the get_direct_stream_link method returns a string.
        """
        pytest.skip("Skipping test_get_direct_stream_link_returns_string")
        alldebrid = AllDebrid(apikey=apikey)
        link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        direct_link = alldebrid.get_direct_stream_link(link=link)
        assert isinstance(direct_link, str)

    def test_get_direct_stream_link_returns_none(self):
        """
        Shiver me timbers! This test be checkin' if the get_direct_stream_link method returns none when given an invalid link.
        """
        alldebrid = AllDebrid(apikey=apikey)
        link = "http://invalid_link.com"
        direct_link = alldebrid.get_direct_stream_link(link=link)
        assert direct_link is None

    def test_get_direct_stream_link_with_multiple_links_returns_list_of_strings(self):
        """
        Arrr! This test be checkin' if the get_direct_stream_link method returns a list of direct links when given multiple links.
        """
        pytest.skip("Skipping test_get_direct_stream_link_with_multiple_links_returns_list_of_strings")
        alldebrid = AllDebrid(apikey=apikey)
        links = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=oHg5SJYRHA0"]
        direct_links = alldebrid.get_direct_stream_link(link=links)
        assert isinstance(direct_links, list)
        assert all(isinstance(link, str) for link in direct_links)

    def test_purge_recent_links_returns_dict(self):
        """
        Arrr! This test be checkin' if the purge_recent_links method returns a dict.
        """
        alldebrid = AllDebrid(apikey=apikey)
        assert isinstance(alldebrid.purge_recent_links(), dict)

    def test_check_pin_status(self):
        """
        Arrr! This test be checkin' if the check_pin_status method returns a dict.
        """
        alldebrid = AllDebrid(apikey=apikey)
        pin = alldebrid.get_pin()
        check_pin = alldebrid.check_pin(pin_response=pin)
        assert isinstance(check_pin, dict)
        assert check_pin.get("status") == "success"

    def test_check_pin_status_with_invalid_pin(self):
        """
        Arrr! This test be checkin' if the check_pin_status method raises a ValueError when given an invalid pin.
        """
        alldebrid = AllDebrid(apikey=apikey)
        with pytest.raises(ValueError):
            alldebrid.check_pin(pin="invalid_pin", hash_value="invalid_hash")
