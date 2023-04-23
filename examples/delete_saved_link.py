import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

link_to_delete = ""

delete_saved_link = alldebrid.delete_saved_link(links=link_to_delete)

print(delete_saved_link)
# Expected response:
# {'status': 'success', 'data': {'message': 'Links were successfully deleted'}}

list_of_links_to_delete = [
    "",
    ""
]

delete_saved_link = alldebrid.delete_saved_link(links=list_of_links_to_delete)

print(delete_saved_link)
# Expected response:
# {'status': 'success', 'data': {'message': 'Links were successfully deleted'}}
