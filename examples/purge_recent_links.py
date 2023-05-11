import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

purged_links = alldebrid.purge_recent_links()

print(purged_links)
# Expected response:
# {'status': 'success', 'data': {'message': 'Recent links history was successfully purged'}}
