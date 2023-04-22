#pylint: disable=C0114
import os, time
from pprint import pprint
from dotenv import load_dotenv
from alldebrid import AllDebrid
from errors import APIError
from utils import handle_exceptions

# Load environment variables from .env file
load_dotenv()

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

# Ping!
#ping = alldebrid.ping()
#pprint('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}
#pprint('Ping:', ping.get('status'))

link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@handle_exceptions(exceptions=(ValueError, APIError))
def get_direct_stream_link(link: str) -> str:
    """
    Wrapper for streaming links.

    Parameters
    ----------
    link : str
        The link to the video to be streamed.

    Returns
    -------
    str
        The direct link to stream the video.

    Raises
    ------
    ValueError
        If the endpoint is not found.
    APIError
        If the API returns an error.
    """
    # TODO: Support multiple links in a list
    if not isinstance(link, str) or not link or isinstance(link, list):
        raise ValueError("Link must be a string.")

    unlock_response = alldebrid.download_link(link)
    data_id = unlock_response["data"]["id"]
    stream_id = unlock_response["data"]["streams"][0]["id"]
    
    stream_response = alldebrid.streaming_links(link, data_id, stream_id)
    
    while True:
        delayed_link_response = alldebrid.delayed_links(
            download_id=stream_response["data"]["delayed"]
        )
        
        status = delayed_link_response["data"]["status"]
        if status == 1:
            break
        elif status == 2:
            delayed_link = delayed_link_response["data"]["link"]
            return delayed_link
        else:
            time.sleep(2)
            continue
    return None

pprint(get_direct_stream_link(link=link))
