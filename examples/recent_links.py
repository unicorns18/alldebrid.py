import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

recent_links = alldebrid.recent_links()

print(recent_links)
# Expected response:
# {'status': 'success', 'data': {'links': [{'link': '', 'link_dl': '', 'filename': '', 'size': 0, 'date': 0, 'host': ''}
