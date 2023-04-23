import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from alldebrid import AllDebrid
from dotenv import load_dotenv

load_dotenv()

alldebrid = AllDebrid(apikey=os.getenv("ALLDEBRID_API_KEY"))

user = alldebrid.user()

print(user)
# Expected response:
# {'status': 'success', 'data': {'user': {'username': '', 'email': '', 'isPremium': True, 'isTrial': False, 'isSubscribed': True, 'premiumUntil': 1684431861, 'lang': 'en', 'preferedDomain': 'com', 'fidelityPoints': 0, 'limitedHostersQuotas': {'ddl': 1000, 'dropapk': 1000, 'dropgalaxy': 2000, 'fileal': 2000, 'filefactory': 3000, 'filespace': 1000, 'flashbit': 5000, 'gigapeta': 3000, 'isra': 5000, 'katfile': 3000, 'vipfile': 1000, 'wipfiles': 3000}, 'notifications': []}}}
