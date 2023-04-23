import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

link_to_save = ""

save_new_link = alldebrid.save_new_link(link=link_to_save)

print(save_new_link)
# Expected response:
# {'status': 'success', 'data': {'message': 'Link was successfully saved'}}

list_of_links_to_save = [
    "",
    "",
    ""
]

save_new_link = alldebrid.save_new_link(link=list_of_links_to_save)

print(save_new_link)
# Expected response:
# {'status': 'success', 'data': {'message': 'Links were successfully saved'}}
