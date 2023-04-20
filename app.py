#pylint: disable=C0114
import os
from dotenv import load_dotenv
from alldebrid import AllDebrid

# Load environment variables from .env file
load_dotenv(dotenv_path='.env', verbose=True)

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('APIKEY'))

# Ping!
ping = alldebrid.ping()
print('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}
