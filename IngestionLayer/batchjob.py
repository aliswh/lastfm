from googlestorage import *
from pylastsource import *
from config import *

storage = GoogleStorage(creds_path, bucket_name)
source = PyLastSource(AUTH_DATA)

SEED_USER = 'dars4'
users = source.get('users',SEED_USER)
for json_user in users:
    storage.write(json_user, f'user_{json_user.id}')
    json_recent_tracks = source.get('recent_tracks',json_user.name)
    storage.write(json_recent_tracks, f'user_{json_user.id}_recent_tracks')
    for track in json_recent_tracks:
        json_track = source.get('track', track.artist, track.title)
        storage.write(json_track, f'track_{json_track.id}')
