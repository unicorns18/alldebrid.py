#pylint: disable=C0114
import os
from pprint import pprint
from dotenv import load_dotenv
from alldebrid import AllDebrid

# Load environment variables from .env file
load_dotenv()

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

# # Ping!
ping = alldebrid.ping()
pprint('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}
