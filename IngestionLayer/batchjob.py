from googlestorage import *
from pylastsource import *
from config import *

storage = GoogleStorage(creds_path, bucket_name)
source = PyLastSource(AUTH_DATA)

users = source.get('users',False,'alishw')
for json_user in users:
    storage.write(json_user, f'user_{json_user.id}')
    json_recent_tracks = source.get('recent_tracks', False,json_user.id)
    storage.write(json_recent_tracks, f'user_{json_user.id}_recent_tracks')
    for track in json_recent_tracks:
        json_track = source.get('track', False, track.artist, track.title)
        storage.write(json_track, f'track_{json_track.id}')
