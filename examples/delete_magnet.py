import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

magnet = ""

magnet_upload = alldebrid.upload_magnets(magnets=magnet)

magnet_id = magnet_upload["data"]["magnets"][0]["id"]

magnet_instant = alldebrid.delete_magnet(magnet_id=magnet_id)

print(magnet_instant)
# Expected response:
# {'status': 'success', 'data': {'message': 'Magnet was successfully deleted'}}
