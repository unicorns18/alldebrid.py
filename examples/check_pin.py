import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

get_pin = alldebrid.get_pin()

check_pin = alldebrid.check_pin(pin_response=get_pin)

print(check_pin)
# Expected response:
# {'status': 'success', 'data': {'activated': False, 'expires_in': 599}}
# NOTE: expires_in is in seconds (599 = 9 minutes and 59 seconds)
