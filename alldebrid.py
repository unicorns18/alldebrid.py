#pylint: disable=C0301
"""
The AllDebrid class is designed to interact with the AllDebrid API. It takes an API key as a parameter and provides methods to make requests to various endpoints of the API. The class can be used to ping the API, get a pin, check a pin, get user information, unlock download links, get streaming links, upload magnets and files, check magnet status, delete magnets, restart magnets, check magnet instant, get saved links, save new links, delete saved links, get recent links, and purge recent links.

Classes
-------
AllDebrid
    Class for interacting with the AllDebrid API.

Fields
------
apikey: str

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
AllDebridError
    Raised when an error occurs with the API.

Examples
--------
>>> import alldebrid
>>> ad = alldebrid.AllDebrid(apikey="YOUR_API_KEY")
>>> ad.ping()
{'status': 'success', 'data': {'ping': 'pong'}}
"""
from typing import Any, Dict, List, Optional, Union
import requests

HOST = "http://api.alldebrid.com/v4/"

apiErrors = {
    'GENERIC': 'An error occurred',
    '404': "Endpoint doesn't exist",

    'AUTH_MISSING_AGENT': "You must send a meaningful agent parameter, see api docs",
    'AUTH_BAD_AGENT': "Bad agent",
    'AUTH_MISSING_APIKEY': 'The auth apikey was not sent',
    'AUTH_BAD_APIKEY': 'The auth apikey is invalid',
    'AUTH_BLOCKED': 'This apikey is geo-blocked or ip-blocked',
    'AUTH_USER_BANNED': 'This account is banned',

    'LINK_IS_MISSING': 'No link was sent',
    'LINK_HOST_NOT_SUPPORTED': 'This host or link is not supported',
    'LINK_DOWN': 'This link is not available on the file hoster website',
    'LINK_PASS_PROTECTED': 'Link is password protected',
    'LINK_HOST_UNAVAILABLE': 'Host under maintenance or not available',
    'LINK_TOO_MANY_DOWNLOADS': 'Too many concurrent downloads for this host',
    'LINK_HOST_FULL': 'All servers are full for this host, please retry later',
    'LINK_HOST_LIMIT_REACHED': "You have reached the download limit for this host",
    'LINK_ERROR': 'Could not unlock this link',

    'REDIRECTOR_NOT_SUPPORTED': 'Redirector not supported',
    'REDIRECTOR_ERROR': 'Could not extract links',

    'STREAM_INVALID_GEN_ID': 'Invalid generation ID',
    'STREAM_INVALID_STREAM_ID': 'Invalid stream ID',

    'DELAYED_INVALID_ID': "This delayed link id is invalid",

    'FREE_TRIAL_LIMIT_REACHED': 'You have reached the free trial limit (7 days // 25GB downloaded or host ineligible for free trial)', #pylint: disable=C0301
    'MUST_BE_PREMIUM': "You must be premium to process this link",

    'MAGNET_INVALID_ID': 'This magnet ID does not exists or is invalid',
    'MAGNET_INVALID_URI': "Magnet is not valid",
    'MAGNET_INVALID_FILE': "File is not a valid torrent",
    'MAGNET_FILE_UPLOAD_FAILED': "File upload failed",
    'MAGNET_NO_URI': "No magnet sent",
    'MAGNET_PROCESSING': "Magnet is processing or completed",
    'MAGNET_TOO_MANY_ACTIVE': "Already have maximum allowed active magnets (30)",
    'MAGNET_MUST_BE_PREMIUM': "You must be premium to use this feature",
    'MAGNET_NO_SERVER': "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.", #pylint: disable=C0301
    'MAGNET_TOO_LARGE': "Magnet files are too large (max 1TB)",

    'PIN_ALREADY_AUTHED': "You already have a valid auth apikey",
    'PIN_EXPIRED': "The pin is expired",
    'PIN_INVALID': "The pin is invalid",

    'USER_LINK_MISSING': "No link provided",
    'USER_LINK_INVALID': "Can't save those links",

    'NO_SERVER': "Server are not allowed to use this feature. Visit https://alldebrid.com/vpn if you're using a VPN.", #pylint: disable=C0301

    'MISSING_NOTIF_ENDPOINT': 'You must provide an endpoint to unsubscribe',

    'VOUCHER_DURATION_INVALID': 'Invalid voucher duration (must be either 15, 30, 90, 180 or 365)',
    'VOUCHER_NB_INVALID': 'Invalid voucher number, must be between 1 and 10',
    'NO_MORE_VOUCHER': 'No voucher of this type available in your account',
    'INSUFFICIENT_BALANCE': 'Your current reseller balance is not enough to generate the requested vouchers', #pylint: disable=C0301
}
endpoints = {
    "Ping": "ping",
    "Get pin": "pin/get",
    "Check pin": "pin/check",
    "User": "user",
    "Download link": "link/unlock",
    "Streaming links": "link/streaming",
    "Delayed links": "link/delayed",
    "Upload magnet": "magnet/upload",
    "Upload file": "magnet/upload/file",
    "Status": "magnet/status",
    "Delete": "magnet/delete",
    "Restart": "magnet/restart",
    "Instant": "magnet/instant",
    "Saved links": "user/links",
    "Save a link": "user/links/save",
    "Delete saved link": "user/links/delete",
    "Recent links": "user/history",
    "Purge history": "user/history/delete"
}

class AllDebridError(Exception):
    """
    Alldebrid error
    """
    code: str
    message: str

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return f'{self.code} - {self.message}'

class AllDebrid:
    """
    Class for interacting with the AllDebrid API.

    Parameters
    ----------
    apikey : str
        The API key to use for the requests.
    """

    def __init__(self, apikey: str) -> None:
        """
        __init__ method for the AllDebrid class.
        """
        self.apikey = apikey

    def ping(self) -> dict:
        """
        Makes a request to the ping endpoint.
        
        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Ping")
        if endpoint is None:
            raise ValueError("Endpoint not found")

        return self._request(method="GET", endpoint=endpoint)
    
    def get_pin(self) -> dict:
        """
        Makes a request to the get pin endpoint.

        Returns
        -------
        dict
            The response from the API.

        Raises
        ------
        requests.exceptions.Timeout
            If the request times out.
        """
        endpoint = endpoints.get("Get pin")
        if endpoint is None:
            raise ValueError("Endpoint not found")

        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response
    
    def check_pin(self, get_pin_response=None, hash=None, pin=None) -> dict:
        """
        Makes a request to the check pin endpoint.

        Parameters
        ----------
        get_pin_response : dict
            The response from the get pin endpoint.
        pin : str
            The pin to check.
        hash : str
            The hash to check.

        Returns
        -------
        dict
            The response from the API.
        """
        if get_pin_response is None and (hash is None or pin is None):
            raise ValueError("Either get_pin_response or hash and pin must be provided")

        params = {
            "check": hash,
            "pin": pin,
            "agent": "python"
        }

        endpoint = endpoints.get("Check pin")
        if endpoint is None:
            raise ValueError("Endpoint not found for Check pin")
        
        response = self._request(method="GET", endpoint=endpoint, params=params)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response
    
    def user(self) -> dict:
        """
        Makes a request to the user endpoint.

        Returns
        -------
        dict
            The response from the API.
        """
        if self.apikey is None:
            raise ValueError("API key is required for this endpoint")
        
        endpoint = endpoints.get("User")
        if endpoint is None:
            raise ValueError("Endpoint not found for User")

        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            if response["error"]["code"] == "AUTH_MISSING_APIKEY":
                raise ValueError("API key is required for this endpoint")
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response
    
    def download_link(self, links: Union[str, List[str]]) -> dict:
        """
        Makes a request to the download link endpoint.

        Parameters
        ----------
        links : Union[str, List[str]]
            The link(s) to unlock.

        Returns
        -------
        dict
            The response from the API.
        """
        # TODO: Support passwords for links, if it has one.

        if isinstance(links, str):
            links = [links]
        params = {
            "link": links,
            "agent": "python"
        }

        endpoint = endpoints.get("Download link")
        if endpoint is None:
            raise ValueError("Endpoint not found for Download link")
        
        response = self._request(method="GET", endpoint=endpoint, params=params)
        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def streaming_links(self, link: List[str]) -> dict:
        """
        Makes a request to the streaming links endpoint.

        Parameters
        ----------
        link : List[str]
            The link to unlock.

        Returns
        -------
        dict
            The response from the API.
        """
        # TODO: Add a stream id (from link/unlock)
        params = {
            "link": link,
            "agent": "python"
        }

        endpoint = endpoints.get("Streaming links")
        if endpoint is None:
            raise ValueError("Endpoint not found for Streaming links")

        response = self._request(method="GET", endpoint=endpoint, params=params)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])

        return response
    
    def delayed_links(self, id: str) -> dict: # pylint: disable=redefined-builtin,C0103
        """
        Makes a request to the delayed links endpoint.

        Notes
        -----
        The id is the id of the link returned from the download link endpoint.
        (download_link method)

        Parameters
        ----------
        id : str
            The id of the link to check.

        Returns
        -------
        dict
            The response from the API.
        """
        if id is None:
            raise ValueError("ID not found for delayed links")
        
        endpoint = endpoints.get("Delayed links")

        if endpoint is None:
            raise ValueError("Endpoint not found for Delayed links")
        
        response = self._request(method="GET", endpoint=endpoint, params={"id": id})

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
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
        """
        params = {
            "magnets": magnets,
            "agent": "python"
        }

        endpoint = endpoints.get("Upload magnet")
        if endpoint is None:
            raise ValueError("Endpoint not found for Upload magnets")
        
        response = self._request(method="POST", endpoint=endpoint, params=params)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def upload_file(self, files: str) -> dict:
        """
        Makes a request to the upload file endpoint.

        Parameters
        ----------
        files : str
            The files to upload.

        Returns
        -------
        dict
            The response from the API.
        """
        if not files:
            raise ValueError("No files to upload")

        # TODO: Support multiple files at once
        file = {'files[0]': open(files, 'rb')}

        endpoint = endpoints.get("Upload file")
        if endpoint is None:
            raise ValueError("Endpoint not found for Upload file")

        response = self._request(method="POST", endpoint=endpoint, files=file)

        return response

    def get_magnet_status(self, magnet_id: Optional[int] = None) -> dict:
        """
        Makes a request to the magnet status endpoint.

        Parameters
        ----------
        magnet_id : Optional[int]
            The magnet id to check.
        status : Optional[str]
            The status of the magnet.
        
        Returns
        -------
        dict
            The response from the API.
        
        Example
        -------
            >>> # magnet is the magnet id returned from the upload magnets endpoint.
            >>> magnet_id = upload['data']['files'][0]['id']
            >>> magnet_status = ad.get_magnet_status(magnet_id=magnet_id)
            >>> print(json.dumps(magnet_status, indent=4, sort_keys=True))
        """
        if magnet_id is None:
            raise ValueError("Magnet ID not found for magnet status")
        
        endpoint = endpoints.get("Status")
        if endpoint is None:
            raise ValueError("Endpoint not found for Magnet status")

        response = self._request(method="GET", endpoint=endpoint, params={"id": magnet_id})

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def delete_magnet(self, magnet_id: int) -> dict:
        """
        Makes a request to the delete magnet endpoint.

        Parameters
        ----------
        magnet_id : int
            The magnet id to delete.

        Returns
        -------
        dict
            The response from the API.

        Example
        -------
            >>> # magnet is the magnet id returned from the upload magnets endpoint.
            >>> magnet_id = upload['data']['files'][0]['id']
            >>> deleted = ad.delete_magnet(magnet_id=magnet_id)
            >>> print(json.dumps(deleted, indent=4, sort_keys=True))
        """
        if magnet_id is None:
            raise ValueError("Magnet ID not found for delete magnet")
        
        endpoint = endpoints.get("Delete")
        if endpoint is None:
            raise ValueError("Endpoint not found for delete magnet")

        response = self._request(method="GET", endpoint=endpoint, params={"id": magnet_id})

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def restart_magnet(self, id: Optional[int] = None, ids: Optional[List[int]] = None) -> dict:
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

        Example
        -------
            >>> # magnet is the magnet id returned from the upload magnets endpoint.
            >>> magnet_id = upload['data']['files'][0]['id']
            >>> restarted = ad.restart_magnet(id=magnet_id)
            >>> print(json.dumps(restarted, indent=4, sort_keys=True))
        """
        if id is None and ids is None:
            raise ValueError("Magnet ID not found for restart magnet")
        
        endpoint = endpoints.get("Restart")
        if endpoint is None:
            raise ValueError("Endpoint not found for restart magnet")
        if id is not None:
            response = self._request(method="GET", endpoint=endpoint, params={"id": id})
        else:
            response = self._request(method="GET", endpoint=endpoint, params={"ids": ids})
            
        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def check_magnet_instant(self, magnets: Optional[Union[str, List[str]]] = None) -> dict:
        """
        Makes a request to the check magnet instant endpoint.

        Parameters
        ----------
        magnets : Optional[Union[str, List[str]]]
            The magnets to check.

        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Instant")
        if endpoint is None:
            raise ValueError("Endpoint not found for check magnet instant")

        if magnets is None:
            raise ValueError("No magnets to check")
        
        if isinstance(magnets, str):
            magnets = [magnets]
        
        response = self._request(method="POST", endpoint=endpoint, magnets=magnets)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response
    
    def saved_links(self) -> dict:
        """
        Makes a request to the saved links endpoint.

        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Saved links")
        if endpoint is None:
            raise ValueError("Endpoint not found for saved links")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def save_new_link(self, link_id: Optional[Union[str, List[str]]]) -> dict:
        """
        Makes a request to the save new link endpoint.

        Parameters
        ----------
        link_id : Optional[Union[str, List[str]]]
            The link id to save.

        Returns
        -------
        dict
            The response from the API.
        """
        if link_id is None:
            raise ValueError("No link id to save")

        endpoint = endpoints.get("Save a link")
        if endpoint is None:
            raise ValueError("Endpoint not found for save new link")
        
        response = self._request(method="POST", endpoint=endpoint, links=link_id)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def delete_saved_link(self, links: Optional[List[str]] = None) -> dict:
        """
        Makes a request to the delete saved link endpoint.

        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Delete saved link")
        if endpoint is None:
            raise ValueError("Endpoint not found for delete saved link")
        
        response = self._request(method="POST", endpoint=endpoint, links=links)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def recent_links(self) -> dict:
        """
        Makes a request to the recent links endpoint.

        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Recent links")
        if endpoint is None:
            raise ValueError("Endpoint not found for recent links")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

    def purge_recent_links(self):
        """
        Makes a request to the purge recent links endpoint.

        Returns
        -------
        dict
            The response from the API.
        """
        endpoint = endpoints.get("Purge history")
        if endpoint is None:
            raise ValueError("Endpoint not found for purge recent links")
        
        response = self._request(method="GET", endpoint=endpoint)

        if response.get("status") == "error":
            raise AllDebridError(response["error"]["code"], response["error"]["message"])
        
        return response

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
        Send a request to the server.

        Parameters
        ----------
        endpoint: str
            Endpoint of server.
        agent: str (default: "python")
            User agent.
        params: dict (default: None)
            Query params.
        files: dict (default: None)
            Files to upload.
        magnets: str (default: None)
            List of magnets to upload.
        timeout: int (default: 10)
            Timeout in seconds.

        Returns
        -------
        dict
            Server Response.
        """
        auth_header = {"Authorization": "Bearer " + self.apikey}
        session = requests.Session()

        if params is None:
            params = {}
        if files is None:
            files = {}
        if magnets is None:
            magnets = []
        if links is None:
            links = []

        if endpoint is None:
            raise ValueError("Endpoint not found for " + endpoint)

        url = HOST + endpoint + "?agent=" + agent

        try:
            if method == "GET":
                response = session.get(
                    url,
                    headers=auth_header,
                    params=params,
                    files=files,
                    timeout=timeout,
                    data=magnets
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
                    response = session.post(
                        url,
                        headers=auth_header,
                        params=params,
                        files=files,
                        timeout=timeout,
                        data=links
                    )
        
        except requests.exceptions.RequestException as exception:
            raise ValueError(apiErrors['GENERIC'] + ': ' + str(exception)) from exception
        
        return response.json()
