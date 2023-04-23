import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

magnet = "some magnet"

magnet_instant = alldebrid.check_magnet_instant(magnets=magnet)

print(magnet_instant)
# Expected response:
# {'status': 'success', 'data': {'magnets': [{'magnet': '', 'hash': '', 'instant': True, 'files': [{'n': 'file.mkv', 's': 5789719166}]}]}}
# Hint: s is the size of the file in bytes ;)

# Prefer to check a ton of magnets at once?
list_of_magnets = [
    "magnet1",
    "magnet2",
    "magnet3"
]

magnet_instant = alldebrid.check_magnet_instant(magnets=list_of_magnets)

print(magnet_instant)
# Expected response:
# {'status': 'success', 'data': {'magnets': [{'magnet': '', 'hash': '', 'instant': True, 'files': [{'n': 'file.mkv', 's': 5789719166}]}, {'magnet': '', 'hash': '', 'instant': True, 'files': [{'n': 'file.mkv', 's': 5789719166}]}, {'magnet': '', 'hash': '', 'instant': True, 'files': [{'n': 'file.mkv', 's': 5789719166}]}]}}
