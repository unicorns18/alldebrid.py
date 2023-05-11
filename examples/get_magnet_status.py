import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

magnet_id = 186561238 # Use your own magnet_id but feel free to use this one :)

magnet_status = alldebrid.get_magnet_status(magnet_id=magnet_id)

print(magnet_status)
