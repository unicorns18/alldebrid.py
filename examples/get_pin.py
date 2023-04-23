import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

get_pin = alldebrid.get_pin()

print(get_pin)
# Expected response:
# {'status': 'success', 'data': {'pin': '', 'check': '', 'expires_in': 600, 'user_url': 'https://alldebrid.com/pin/?pin=', 'base_url': 'https://alldebrid.com/pin/', 'check_url': ''}}
# NOTE: expires_in is in seconds (600 = 10 minutes)
