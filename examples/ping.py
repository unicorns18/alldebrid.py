import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an instance of AllDebrid
alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

# Ping!
ping = alldebrid.ping()
print('Ping:', ping)
# Ping: {'status': 'success', 'data': {'ping': 'pong'}}
