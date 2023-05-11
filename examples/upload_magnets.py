import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

single_magnet = ""

magnet_upload = alldebrid.upload_magnets(magnets=single_magnet)

print(magnet_upload)

list_of_magnets = [
    "",
    "",
    ""
]

for x in list_of_magnets:
    magnet_upload = alldebrid.upload_magnets(magnets=x)

print(magnet_upload)
