#pylint: disable=C0114
import os
from pprint import pprint
from dotenv import load_dotenv
from alldebrid import AllDebrid

# Load environment variables from .env file
load_dotenv()

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

# Ping!
ping = alldebrid.ping()
pprint('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}

LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
list_of_links = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=2ZIpFytCSVc"
]

pprint(alldebrid.get_direct_stream_link(list_of_links))
