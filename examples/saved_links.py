import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv('ALLDEBRID_API_KEY'))

saved_links = alldebrid.saved_links() # returns a dict
if saved_links == {}:
    print("No saved links found")
    exit()
link = saved_links['data']['links'][0]['link'] # returns a string
print(link)
deleted_link = alldebrid.delete_saved_link(links=link)
print(deleted_link)

# Accessing one link
one_link = saved_links['data']['links'][0]["link"]
print(one_link)

# Accessing all links
for link in saved_links['data']['links']:
    print(link["link"])
