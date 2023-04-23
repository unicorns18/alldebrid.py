import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

file = ["file_path"]

file_upload = alldebrid.upload_file(file_paths=file)

print(file_upload)
# Expected response:
# {'status': 'success', 'data': {'files': [{'file': '', 'name': '', 'size': 56886841835, 'hash': '', 'ready': True, 'id': 186561241}]}}

# Upload multiple files
# Change the path to your own path
for file in os.listdir("../"):
    if file.endswith(".torrent"): 
        # Change the path to your own path
        list_of_files = [os.path.join("../", file)]
        file_upload = alldebrid.upload_file(file_paths=list_of_files)
        print(file_upload)
        # Expected response: (for each file)
        # {'status': 'success', 'data': {'files': [{'file': '', 'name': '', 'size': 56886841835, 'hash': '', 'ready': True, 'id': 186561241}]}}
