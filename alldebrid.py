#pylint: disable=C0301
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
import time
from typing import Any, Dict, List, Optional, Union
import requests
from errors import APIError
from endpoints import endpoints
from utils import handle_exceptions

API_HOST = "http://api.alldebrid.com/v4/"

class AllDebrid:
    """
    Class for interacting with the AllDebrid API.

    Parameters
    ----------
    apikey : str
        The API key to use for the requests.
    """

    def __init__(self, apikey: str, proxy: Optional[str] = None) -> None:
        """
        __init__ method for the AllDebrid class.
        """
        self.apikey = apikey
        self.proxy = proxy

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
        endpoint = endpoints.get("ping")
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
        endpoint = endpoints.get("get pin")
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

        endpoint = endpoints.get("check pin")
        if not endpoint:
            raise ValueError("Endpoint not found for Check pin")
        
        response = self._request(method="GET", endpoint=endpoint, params=params)

        if response.get("status") == "error":
            error = response["error"]
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
        endpoint = endpoints.get("user")
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
        endpoint = endpoints.get("download link")
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

        endpoint = endpoints.get("streaming links")
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
        
        endpoint = endpoints.get("delayed links")
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
        
        endpoint = endpoints.get("upload magnet")
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
            
        endpoint = endpoints.get("upload file")
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
        
        endpoint = endpoints.get("status")
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
        
        endpoint = endpoints.get("delete")
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
        
        endpoint = endpoints.get("restart")
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
        endpoint = endpoints.get("instant")
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
        endpoint = endpoints.get("saved links")
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

        endpoint = endpoints.get("save a link")
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
        endpoint = endpoints.get("delete saved link")
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
        endpoint = endpoints.get("recent links")
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
        endpoint = endpoints.get("purge history")
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
        if not isinstance(link, (str, list)):
            raise ValueError("Link must be a string or list of strings.")
        
        if isinstance(link, str):
            links = [link]
        else:
            links = link
        
        direct_links = []
        for link in links:
            unlock_response = self.download_link(link)
            data_id = unlock_response["data"]["id"]
            stream_id = unlock_response["data"]["streams"][0]["id"]

            stream_response = self.streaming_links(link, data_id, stream_id)

            while True:
                delayed_link_response = self.delayed_links(
                    download_id=stream_response["data"]["delayed"]
                )
                
                status = delayed_link_response["data"]["status"]
                if status == 1:
                    break
                elif status == 2:
                    delayed_link = delayed_link_response["data"]["link"]
                    direct_links.append(delayed_link)
                    break
                else:
                    time.sleep(2)
                    continue
        
        if not direct_links:
            return None
        
        if len(direct_links) == 1:
            return direct_links[0]
        
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

        if key_pattern.match(api_key):
            return True
        else:
            return False

    def _request(
            self,
            method: str,
            endpoint: str,
            agent: str = "python",
            params: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            magnets: Optional[str] = None,
            links: Optional[str] = None,
            timeout: int = 10,
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
        timeout: int
            Timeout of the request.

        Returns
        -------
        dict
            Response of the request.
        """
        if not self._check_valid_api_key(self.apikey):
            raise ValueError("Invalid API Key")

        if self.apikey is None or self.apikey == "":
            raise ValueError("API Key not found")

        auth_header = {"Authorization": "Bearer " + self.apikey}
        session = requests.Session()

        if self.proxy is not None:
            session.proxies = {"http": self.proxy, "https": self.proxy}

        params = {} if params is None else params
        files = {} if files is None else files
        magnets = [] if magnets is None else magnets
        links = [] if links is None else links

        if endpoint is None or endpoint not in endpoints.values():
            raise ValueError(f"Invalid endpoint: {endpoint}")

        url = API_HOST + endpoint + "?agent=" + agent

        common_params = {
            'headers': auth_header,
            'params': params,
            'files': files,
            'timeout': timeout
        }

        if method == "GET":
            response = session.request(
                method='GET',
                url=url,
                data=magnets or links,
                **common_params
            )
        elif method == "POST":
            if magnets is not None and len(magnets) > 0:
                if isinstance(magnets, str):
                    magnets = [magnets]
                magnets = {'magnets[]': magnets}
            else:
                magnets = None
            if links is not None and len(links) > 0:
                if isinstance(links, str):
                    links = [links]
                links = {'links[]': links}
            else:
                links = None
            response = session.request(
                method='POST',
                url=url,
                data=magnets or links,
                **common_params
            )

        if response.status_code == 200:
            return response.json()
        raise APIError(response.status_code, response.text)
