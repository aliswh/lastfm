from ingestion_layer.pylastsource import *
from ingestion_layer.config import *
import time
from datetime import datetime


### EXAMPLES, DELETE
p = PyLastSource(AUTH_DATA)

onemonthago = p.timestamp_x_days_ago(10)
print(datetime.fromtimestamp(onemonthago))

SEED_USER = 'dars4' # random user name found on last.fm
user = p.network.get_user(SEED_USER)
user_json = p.get('user', SEED_USER)
print(user_json)

track_json = p.get('track', 'Charli XCX', 'Vroom Vroom')
print(track_json)

user_tracks_json = p.get('recent_tracks', SEED_USER, limit=10,  time_to=onemonthago)
print(user_tracks_json)

user_pool_json = p.get('user_pool', SEED_USER, MAX=10)
print(user_pool_json)