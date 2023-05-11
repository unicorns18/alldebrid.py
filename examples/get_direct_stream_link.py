import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid.alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

# # Singular link
LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

streaming_link = alldebrid.get_direct_stream_link(link=LINK)

# # Multiple links
links = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=L_jWHffIx5E',
    'https://www.youtube.com/watch?v=QH2-TGUlwu4'
]
# # Congrats to you if you recognize the first link ;)

list_of_links = alldebrid.get_direct_stream_link(link=links)

print(list_of_links)
