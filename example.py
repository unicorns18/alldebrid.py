#pylint: disable=C0114
import os
from dotenv import load_dotenv
from alldebrid import AllDebrid
from pprint import pprint

# Load environment variables from .env file
load_dotenv()

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

# Ping!
ping = alldebrid.ping()
print('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}
print('Ping:', ping.get('status'))
