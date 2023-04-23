from typing import Dict
from functools import lru_cache

endpoints = {
    "ping": "ping",
    "get pin": "pin/get",
    "check pin": "pin/check",
    "user": "user",
    "download link": "link/unlock",
    "streaming links": "link/streaming",
    "delayed links": "link/delayed",
    "upload magnet": "magnet/upload",
    "upload file": "magnet/upload/file",
    "status": "magnet/status",
    "delete": "magnet/delete",
    "restart": "magnet/restart",
    "instant": "magnet/instant",
    "saved links": "user/links",
    "save a link": "user/links/save",
    "delete saved link": "user/links/delete",
    "recent links": "user/history",
    "purge history": "user/history/delete"
}

@lru_cache(maxsize=None, typed=False)
def get_endpoints() -> Dict[str, str]:
    """
    Returns a dictionary of the endpoints for the API.

    Returns
    -------
    Dict[str, str]
        A dictionary of the endpoints for the API.
    """
    return endpoints
