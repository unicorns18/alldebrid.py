#pylint: disable=C0301,C0302
"""
The AllDebrid class is designed to interact with the AllDebrid API. It takes an API key as a parameter and provides methods to make requests to various endpoints of the API. The class can be used to ping the API, get a pin, check a pin, get user information, unlock download links, get streaming links, upload magnets and files, check magnet status, delete magnets, restart magnets, check magnet instant, get saved links, save new links, delete saved links, get recent links, and purge recent links.

Classes
-------
AllDebrid
    Class for interacting with the AllDebrid API.

Fields
------
- apikey: str
    The API key to use for the requests.
- proxy: Optional[str]
    The proxy to use for the requests.

Functions
---------
- ping(): Makes a request to the ping endpoint and returns the response from the API.
- get_pin(): Makes a request to the get pin endpoint and returns the response from the API. Raises requests.exceptions.Timeout if the request times out.
- check_pin(): Makes a request to the check pin endpoint and returns the response from the API.
- user(): Makes a request to the user endpoint and returns the response from the API.
- download_link(): Makes a request to the download link endpoint and returns the response from the API.
- streaming_links(): Makes a request to the streaming links endpoint and returns the response from the API.
- delayed_links(): Makes a request to the delayed links endpoint and returns the response from the API.
- upload_magnets(): Makes a request to the upload magnets endpoint and returns the response from the API.
- upload_file(): Makes a request to the upload file endpoint and returns the response from the API.
- get_magnet_status(): Makes a request to the magnet status endpoint and returns the response from the API.
- delete_magnet(): Makes a request to the delete magnet endpoint and returns the response from the API.
- restart_magnet(): Makes a request to the restart magnet endpoint and returns the response from the API.
- check_magnet_instant(): Makes a request to the check magnet instant endpoint and returns the response from the API.
- saved_links(): Makes a request to the saved links endpoint and returns the response from the API.
- save_new_link(): Makes a request to the save new link endpoint and returns the response from the API.
- delete_saved_link(): Makes a request to the delete saved link endpoint and returns the response from the API.
- recent_links(): Makes a request to the recent links endpoint and returns the response from the API.
- purge_recent_links(): Makes a request to the purge recent links endpoint and returns the response from the API.

Exceptions
----------
APIError
    Raised when an error occurs with the API.

Examples
--------
>>> import alldebrid
>>> ad = alldebrid.AllDebrid(apikey="YOUR_API_KEY")
>>> ad.ping()
{'status': 'success', 'data': {'ping': 'pong'}}
"""
import os
import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin
import time
import requests
from errors import APIError, MaxAttemptsExceededException
from endpoints import get_endpoints
from utils import handle_exceptions

API_HOST = "http://api.alldebrid.com/v4/"

class StreamLinkProcessor:
    """
    The StreamLinkProcessor class is designed to process streaming links for video content.
    It takes a downloader, the maximum number of attempts (max_attempts) and a delay, which determines how long to wait between attempts to obtain the desired result from the downloader.
    It contains a single method, get_delayed_link, which attempts to obtain a delayed streaming link from the downloader.
    
    Methods
    -------
    get_delayed_link(link: str) -> Optional[str]
        Attempts to obtain a delayed streaming link from the downloader.

    Parameters
    ----------
    downloader: Any
        The downloader to use to obtain the delayed streaming link.
    max_attempts: int (default=5)
        The maximum number of attempts to make to obtain the delayed streaming link.
    delay: int (default=3)
        The delay between attempts to obtain the delayed streaming link.

    Returns
    -------
    Optional[str]
        The delayed streaming link.

    Raises
    ------
    Exception
        Raised when the maximum number of attempts is reached.
    """

    def __init__(self, downloader: Any, max_attempts: int = 5, delay: int = 3, retry_delay: int = 3, max_delay: int = 30):
        self.downloader = downloader
        self.max_attempts = max_attempts
        self.delay = delay
        self.retry_delay = retry_delay
        self.max_delay = max_delay

    def _try_get_delayed_link(self, link: str, downloader, max_attempts, retry_delay, max_delay) -> Optional[str]:
        """
        Attempts to obtain a delayed streaming link from the downloader for the given streaming content link. This method makes repeated calls to the downloader object to try and obtain the delayed link.

        Args:
            link (str): A link to a streaming content.
            downloader (object): A downloader object.
            max_attempts (int): The maximum number of attempts to obtain the delayed link.
            retry_delay (float): The delay time between each attempt in seconds.
            max_delay (float): The maximum duration of the loop in seconds.

        Returns:
            Optional[str]: The delayed link which can later be used to stream the video, or None if a delayed link 
            could not be obtained.

        Raises:
            TimeoutError: Raised when the maximum time limit to obtain a delayed link has been reached without success.
            Exception: Raised when the maximum number of attempts to obtain a delayed link has been reached without success.
        """
        unlock_response = downloader.download_link(link)
        # data_id = unlock_response["data"]["id"]
        # stream_id = unlock_response["data"]["streams"][0]["id"]
        data_id = unlock_response.get("data", {}).get("id")
        stream_id = unlock_response.get("data", {}).get("streams", [{}])[0].get("id")
        if not data_id or stream_id:
            raise ValueError("Could not obtain data id or stream id.")

        stream_response = downloader.streaming_links(link, data_id, stream_id)

        attempts = 0
        time_limit = max_delay
        start_time = time.time()

        while attempts < max_attempts:
            delayed_link_response = downloader.delayed_links(download_id=stream_response["data"]["delayed"])

            status = delayed_link_response["data"]["status"]
            if status == 2:
                return delayed_link_response["data"]["link"]
            elif status == 1:
                elapsed_time = time.time() - start_time
                if elapsed_time >= time_limit:
                    raise TimeoutError("Max delay reached. Cannot get direct link.")
            time.sleep(retry_delay)
            attempts += 1

        raise MaxAttemptsExceededException("Max attempts reached. Cannot get direct link.")

    def get_delayed_link(self, link: str) -> Optional[str]:
        """
        Attempts to obtain a delayed streaming link from the downloader for the given streaming content link.

        Args:
            link (str): A link to a streaming content.

        Returns:
            Optional[str]: The delayed link which can later be used to stream the video, or None if a delayed link 
            could not be obtained.

        Raises:
            TimeoutError: Raised when the maximum time limit to obtain a delayed link has been reached without success.
            Exception: Raised when the maximum number of attempts to obtain a delayed link has been reached without success.
        """
        try:
            return self._try_get_delayed_link(
                link,
                self.downloader,
                self.max_attempts,
                self.retry_delay,
                self.max_delay
            )                                
        except Exception as exc:
            raise exc
        finally:
            self.downloader.close_connection()

class AllDebrid:
    """
    Class for interacting with the AllDebrid API.

    Parameters
    ----------
    apikey : str
        The API key to use for the requests.
    """

    def __init__(self, apikey: str, proxy: Optional[str] = None, timeout: int = None) -> None:
        """
        __init__ method for the AllDebrid class.
        """
        self.apikey = apikey
        self._authenticated = False
        self.proxy = proxy
        self.auth_header = {"Authorization": "Bearer " + apikey}
        self.base_url = API_HOST
        self.timeout = timeout
        
        self.session = requests.Session()

        self.endpoints = get_endpoints()

    def ping(self) -> dict[str, Any]:
        """
        Makes a request to the ping endpoint.
        
        Returns
        -------
        dict[str, Any]
            The response from the API.

        Raises
        ------
        ValueError
            If the endpoint is not found.
        APIError
            If the API returns an error.
        """
        endpoint = self.endpoints.get("ping")
        if not endpoint:
            raise ValueError("Endpoint not found for ping")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])

        return response
    
    def get_pin(self) -> dict:
        """
        Makes a request to the get pin endpoint.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If the endpoint is not found.
        APIError
            If the API returns an error.
        """
        endpoint = self.endpoints.get("get pin")
        if not endpoint:
            raise ValueError(f"Endpoint {endpoint} not found")

        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response
    
    def check_pin(self, pin_response=None, hash_value=None, pin=None) -> dict:
        """
        Makes a request to the check pin endpoint.

        Parameters
        ----------
        pin_response : dict
            The response from the get pin endpoint.
        pin : str
            The pin to check.
        hash_value : str
            The hash to check.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If neither pin_response nor hash_value and pin are provided.
        APIError
            If the API returns an error.
        """
        if pin_response is None and (hash_value is None or pin is None):
            raise ValueError("Either pin_response or hash and pin must be provided")

        params = {}
        if pin_response is not None:
            params["check"] = pin_response["data"]["check"]
            params["pin"] = pin_response["data"]["pin"]
        else:
            params["hash"] = hash_value
            params["pin"] = pin

        endpoint = self.endpoints.get("check pin")
        if not endpoint:
            raise ValueError("Endpoint not found for Check pin")
        
        response = self._request(method="GET", endpoint=endpoint, params=params)

        if response.get("status") == "error":
            error = response["error"]
            if error["code"] == "PIN_INVALID":
                raise ValueError("Invalid pin")
            raise APIError(error["code"], error["message"])
        
        return response
    
    def user(self) -> dict:
        """
        Makes a request to the user endpoint.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If the API key is not provided.
        APIError
            If the API returns an error.
        """
        endpoint = self.endpoints.get("user")
        if not endpoint:
            raise ValueError("Endpoint not found for User")

        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            error = response["error"]
            if error["code"] == "AUTH_MISSING_APIKEY":
                raise ValueError("API key is required for this endpoint")
            raise APIError(error["code"], error["message"])
        
        return response
    
    def download_link(self, links: Union[str, List[str]], password: Optional[str] = None) -> Dict[str, Any]:
        """
        Makes a request to the download link endpoint.

        Parameters
        ----------
        links : Union[str, List[str]]
            The link(s) to unlock.
        password : Optional[str], optional
            The password for the link, if it has one, by default None

        Returns
        -------
        Dict[str, Any]
            The response from the API.

        Raises
        ------
        ValueError
            If the endpoint is not found.
        APIError
            If the API returns an error.
        """
        endpoint = self.endpoints.get("download link")
        if not endpoint:
            raise ValueError("Endpoint not found for download link")

        if isinstance(links, str):
            links = [links]

        data = {
            "link": links,
            "agent": "python"
        }

        if password:
            data["password"] = password
        
        response = self._request(method="GET", endpoint=endpoint, params=data)
        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def streaming_links(self, link: str, stream_id: str, stream: str) -> dict:
        """
        Makes a request to the streaming links endpoint.

        Parameters
        ----------
        link : str
            The link to unlock.
        stream_id : str
            The link ID you received from the /link/unlock call.
        stream : str
            The stream ID you chose from the stream qualities list returned by /link/unlock.

        Returns
        -------
        dict
            The response from the API.
        
        Raises
        ------
        ValueError
            If the endpoint is not found.
        APIError
            If the API returns an error.
        """
        data = {
            "link": link,
            "agent": "python",
            "id": stream_id,
            "stream": stream
        }

        endpoint = self.endpoints.get("streaming links")
        if not endpoint:
            raise ValueError("Endpoint not found for Streaming links")

        response = self._request(method="GET", endpoint=endpoint, params=data)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])

        return response
    
    def delayed_links(self, download_id: str) -> dict:
        """
        Makes a request to the delayed links endpoint.

        Notes
        -----
        The id is the id of the link returned from the download link endpoint.
        (download_link method)

        Parameters
        ----------
        download_id : str
            The id of the link to check.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If the id is not found.
        APIError
            If the API returns an error.
        """
        if not download_id:
            raise ValueError("ID not found for delayed links")
        
        endpoint = self.endpoints.get("delayed links")
        if not endpoint:
            raise ValueError("Endpoint not found for delayed links")
        
        data = { "id": download_id }

        response = self._request(method="GET", endpoint=endpoint, params=data)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def upload_magnets(self, magnets: List[str]) -> dict:
        """
        Makes a request to the upload magnets endpoint.

        Parameters
        ----------
        magnets : List[str]
            The magnets to upload.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If the magnets are not found.
        APIError
            If the API returns an error.
        """
        if not magnets:
            raise ValueError("Magnets not found for upload magnets")
        
        endpoint = self.endpoints.get("upload magnet")
        if endpoint is None:
            raise ValueError("Endpoint not found for Upload magnets")

        data = {
            "magnets": magnets,
        }
        
        response = self._request(method="POST", endpoint=endpoint, params=data)

        if response.get("status") == "error":
            error = response["error"]
            if error["code"] == "NO_SERVER":
                raise ValueError("API key is required for this endpoint")
            raise APIError(error["code"], error["message"])
        
        return response

    def upload_file(self, file_paths: List[str]) -> dict:
        """
        Makes a request to the upload file endpoint.

        Parameters
        ----------
        file_paths : List[str]
            The files to upload.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        ValueError
            If the file is not found.
        APIError
            If the API returns an error.
        """
        if not file_paths:
            raise ValueError(f"No files to upload. {file_paths}")
        
        for i, file_path in enumerate(file_paths):
            if not isinstance(file_path, str) or not os.path.isfile(file_path):
                raise ValueError(f"File path is not valid. ({i}: {file_path})")
            
        endpoint = self.endpoints.get("upload file")
        if not endpoint:
            raise ValueError("Endpoint not found for Upload file")
        
        files = {}
        for i, file_path in enumerate(file_paths):
            with open(file_path, 'rb') as file:
                files[f"files[{i}]"] = (file.name, file.read(), 'application/x-bittorrent')

        response = self._request(method="POST", endpoint=endpoint, files=files)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def get_magnet_status(self, magnet_id: int) -> dict:
        """
        Makes a request to the magnet status endpoint.

        Parameters
        ----------
        magnet_id : int
            The magnet id to check.
        
        Returns
        -------
        dict
            The response from the API.
        
        Raises
        ------
        APIError
            If the API returns an error.
        ValueError
            If the magnet id is not found.
        """
        if not magnet_id:
            raise ValueError("Magnet ID not found for magnet status")
        
        endpoint = self.endpoints.get("status")
        if not endpoint:
            raise ValueError("Endpoint not found for Magnet status")

        response = self._request(method="GET", endpoint=endpoint, params={"id": magnet_id})

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def delete_magnet(self, magnet_id: Optional[int] = None) -> dict:
        """
        Makes a request to the delete magnet endpoint.

        Parameters
        ----------
        magnet_id : int, optional
            The magnet id to delete.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        APIError
            If the API returns an error.
        ValueError
            If the magnet id is not found.
        """
        if not magnet_id:
            raise ValueError("Magnet ID not found for delete magnet")
        
        endpoint = self.endpoints.get("delete")
        if not endpoint:
            raise ValueError("Endpoint not found for delete magnet")

        response = self._request(method="GET", endpoint=endpoint, params={"id": magnet_id})

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def restart_magnet(self, magnet_id: Optional[int] = None, ids: Optional[List[int]] = None) -> dict:
        """
        Makes a request to the restart magnet endpoint.

        Parameters
        ----------
        id : Optional[int]
            The magnet id to restart.
        ids : Optional[List[int]]
            The magnet ids to restart.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        APIError
            If the API returns an error.
        ValueError
            If no magnet id or ids are provided.
        """
        if magnet_id is None and ids is None:
            raise ValueError("Magnet ID not found for restart magnet")
        if magnet_id is not None and ids is not None:
            raise ValueError("Only one of magnet_id or ids can be provided for restart magnet")
        
        endpoint = self.endpoints.get("restart")
        if not endpoint:
            raise ValueError("Endpoint not found for restart magnet")
        
        params = {}
        if magnet_id is not None:
            params["id"] = magnet_id
        else:
            params["ids"] = ids

        response = self._request(method="GET", endpoint=endpoint, params=params)
                    
        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def check_magnet_instant(self, magnets: Union[str, List[str]] = None) -> dict:
        """
        Check instant availability of magnets.

        Parameters
        ----------
        magnets: Union[str, List[str]]
            Magnets to check.

        Returns
        -------
        dict
            Instant availability of magnets.

        Raises
        ------
        APIError
            If the AllDebrid API returns an error.
        ValueError
            If endpoint is not found.
        """
        endpoint = self.endpoints.get("instant")
        if not endpoint:
            raise ValueError("Endpoint not found for check magnet instant")

        if not magnets:
            raise ValueError("No magnets to check")
        
        if isinstance(magnets, str):
            magnets = [magnets]
        
        response = self._request(method="POST", endpoint=endpoint, magnets=magnets)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response
    
    def saved_links(self) -> dict:
        """
        Get a list of all the links saved in the account.

        Returns
        -------
        dict:
            Links saved in the account.

        Raises
        ------
        APIError
            If request is unsuccessful.
        ValueError
            If endpoint is not found.
        """
        endpoint = self.endpoints.get("saved links")
        if not endpoint:
            raise ValueError("Endpoint not found for saved links")
        
        response = self._request(method="GET", endpoint=endpoint)
        if not response["data"]["links"]:
            return {}
        
        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def save_new_link(self, link: Union[str, List[str]]) -> dict:
        """
        Save a new link.

        Parameters
        ----------
        link: Union[str, List[str]]
            Link id to save.

        Returns
        -------
        dict
            Response of request.

        Raises
        ------
        APIError
            If request is unsuccessful.
        ValueError
            If endpoint is not found.
        """
        if not link:
            raise ValueError("No link id to save")

        endpoint = self.endpoints.get("save a link")
        if not endpoint:
            raise ValueError("Endpoint not found for save new link")
        
        response = self._request(method="POST", endpoint=endpoint, links=link)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def delete_saved_link(self, links: List[str] = None) -> dict:
        """
        Delete saved links.

        Parameters
        ----------
        links: List[str]
            List of links.

        Returns
        -------
        dict
            Response of api.

        Raises
        ------
        APIError
            If request is unsuccessful.
        ValueError
            If endpoint is not found.
        """
        endpoint = self.endpoints.get("delete saved link")
        if not endpoint:
            raise ValueError("Endpoint not found for delete saved link")
        
        response = self._request(method="POST", endpoint=endpoint, links=links)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def recent_links(self) -> dict:
        """
        Get recent links.

        Returns
        -------
        dict
            Returns a dict containing all the recent links.

        Raises
        ------
        APIError
            If any error occurred while getting recent links.
        """
        endpoint = self.endpoints.get("recent links")
        if not endpoint:
            raise ValueError("Endpoint not found for recent links.")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response

    def purge_recent_links(self) -> dict:
        """
        Purge all the recent links.

        Returns
        -------
        dict
            Response of the API.

        Raises
        ------
        APIError
            If any error occurred while purging recent links.
        ValueError
            If the endpoint is not found.
        """
        endpoint = self.endpoints.get("purge history")
        if not endpoint:
            raise ValueError("Endpoint URL not found for purging recent links.")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            error = response["error"]
            raise APIError(error["code"], error["message"])
        
        return response
    
    @handle_exceptions(exceptions=(ValueError, APIError))
    def get_direct_stream_link(self, link: Union[str, List[str]]) -> Union[str, None]:
        """
        Wrapper for streaming links.

        Parameters
        ----------
        link : Union[str, List[str]]
            The link to the video to be streamed.

        Returns
        -------
        Union[str, None]
            The direct link to stream the video.

        Raises
        ------
        ValueError
            If the endpoint is not found.
        APIError
            If the API returns an error.
        """
        self.validate_input(link)

        links = [link] if isinstance(link, str) else link

        direct_links = self.get_direct_links(links, StreamLinkProcessor(self))

        return direct_links[0] if len(direct_links) == 1 else direct_links

    def validate_input(self, link: Any) -> None:
        """
        Checks if the input link is a string or a list of strings. If not, raises a ValueError.

        Args:
            link (Any): A string or a list of strings.

        Returns:
            None

        Raises:
            ValueError: If the link is not a string or a list of strings.
        """
        if not isinstance(link, (str, list)):
            raise ValueError("Link must be a string or list of strings.")

    def get_direct_links(self, links: List[str], processor: StreamLinkProcessor) -> List[str]:
        """
        Given a list of links and a StreamLinkProcessor object, returns a list of delayed links
        that have been processed into direct links.

        Args:
            links (List[str]): A list of delayed links to be processed.
            processor (StreamLinkProcessor): A StreamLinkProcessor object with a method\n            `get_delayed_link(link: str) -> str` that converts delayed links to direct
                links.

        Returns:
            List[str]: A list of processed direct links.
        """
        direct_links = []
        for link in links:
            delayed_link = processor.get_delayed_link(link)
            if delayed_link is not None:
                direct_links.append(delayed_link)

        return direct_links

    def _check_valid_api_key(self, api_key: str) -> bool:
        """
        Check if the API key is valid.

        Parameters
        ----------
        api_key: str
            API key to check.

        Returns
        -------
        bool
            True if the API key is valid, False otherwise.
        """
        if not isinstance(api_key, (str, bytes)):
            raise ValueError("API key must be a str or bytes-like object.")

        key_pattern = re.compile(r'^[a-zA-Z0-9]{20}$')
        try:
            return bool(key_pattern.match(api_key))
        except TypeError:
            return False
        
    def _authenticate(self):
        if not self.apikey or self.apikey is None or self.apikey == "":
            raise ValueError("No API key provided.")
        
        if not self._check_valid_api_key(self.apikey):
            raise ValueError("Invalid API key provided.")
        
        self._authenticated = True
        
    def _get_session(self):
        if self.session is None:
            self.session = requests.Session()

            if self.proxy is not None:
                self.session.proxies = {"http": self.proxy, "https": self.proxy}

        return self.session
    
    def _build_url(self, endpoint: str, agent: str) -> str:
        return urljoin(API_HOST, endpoint) + "?agent=" + agent
    
    def _build_data(self, magnets: Optional[str], links: Optional[str]) -> dict:
        if not magnets:
            magnets = []
        elif isinstance(magnets, str):
            magnets = [magnets]

        if not links:
            links = []
        elif isinstance(links, str):
            links = [links]

        data = {'magnets[]': magnets} if magnets else {'links[]': links}

        return data
    
    def _handle_error(self, response: requests.Response, exc: requests.exceptions.RequestException, status_code: int = 408, message: str = None) -> None:
        if response is not None:
            raise APIError(response.status_code, response.text) from exc
        else:
            raise APIError(status_code, message) from exc
    
    def _send_request(
            self,
            method: str,
            url: str,
            auth_header: dict,
            data: dict,
            params: dict,
            files: dict,
            timeout: int,
            session: requests.Session,
            expected_response: List[int] = None,
        ) -> dict:
        if expected_response is None:
            expected_response = [200]

        common_params = {
            'headers': auth_header,
            'params': params,
            'files': files,
            'timeout': timeout
        }

        try:
            response = session.request(
                method=method,
                url=url,
                data=data,
                **common_params
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            self._handle_error(response, exc)
        except requests.exceptions.Timeout as exc:
            self._handle_error(response, exc, status_code=408, message="Request timed out.")
        except requests.exceptions.ConnectionError as exc:
            self._handle_error(response, exc, status_code=503, message="Failed to connect to AllDebrid's API.")
        except requests.exceptions.RequestException as exc:
            self._handle_error(response, exc, status_code=408, message=f"Failed to connect to AllDebrid's API: {url}. Error message: {exc}")

        if response.status_code not in expected_response:
            raise APIError(response.status_code, response.text)

        return response.json()
    
    def close_connection(self):
        """
        Close the connection to the API.
        """
        if self.session is not None:
            self.session.close()
                
    def _request(
            self,
            method: str,
            endpoint: str,
            agent: str = "python",
            params: Union[Dict[str, Any], None] = None,
            files: Union[Dict[str, Any], None] = None,
            magnets: Optional[str] = None,
            links: Optional[str] = None,
        ) -> dict:
        """
        Make the request to the API.

        Parameters
        ----------
        method: str
            Method of the request.
        endpoint: str
            Endpoint of the request.
        agent: str
            User Agent.
        params: Optional[Dict[str, Any]]
            Parameters of the request.
        files: Optional[Dict[str, Any]]
            Files of the request.
        magnets: Optional[str]
            Magnets of the request.
        links: Optional[str]
            Links of the request.
        Returns
        -------
        dict
            Response of the request.
        """
        if not self._authenticated:
            self._authenticate()

        url = self._build_url(endpoint, agent)
        data = self._build_data(magnets, links)
        session = self._get_session()
        timeout = self.timeout if self.timeout is not None else 10

        response = self._send_request(
            method=method,
            url=url,
            auth_header=self.auth_header,
            data=data,
            params=params,
            files=files,
            timeout=timeout,
            session=session,
        )

        return response
