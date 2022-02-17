from .abstract_ingestion_layer import Writer

class BatchWriter(Writer):
    def __init__(self, source, destination):
        self.source = source
        self.dest = destination

    def write(self, dest_path, seed_user, users_limit, tracks_limit, debug = False):
        users = self.source.get('user_pool',seed_user,MAX=users_limit)
        for user in users:
            if debug:
                print(f'[User] {user}')
            self.dest.write(user, dest_path+f"users/user_{user['id']}")
            recent_tracks = self.source.get('recent_tracks',user['user'],limit=tracks_limit)
            self.dest.write(recent_tracks, dest_path+f"recent_tracks/user_recent_tracks_{user['id']}")
            for track in recent_tracks[1:]:
                track = self.source.get('track', track['artist'], track['title'])
                artist = self.source.get('artist', track['artist'])
                self.dest.write(track, dest_path+f"tracks/track_{track['id']}")
                self.dest.write(artist, dest_path+f"artists/artist_{artist['id']}")
                if debug:
                    print(f'[Track] {track}')
                    print(f'[Artist] {artist}')
                    print()