import requests
import json
import pylast
import hashlib
from datetime import datetime, date, timedelta

from .abstract_ingestion_layer import Source

TAG_LIMIT = 5

class PyLastSource(Source):
  def __init__(self, AUTH_DATA:dict):
    ''' Initialization of 'Network' object from PyLast.
    
    Args: dictionary w/ all authentication data, which includes:
      -  API_KEY,
      -  API_SECRET,
      -  username,
      -  password

    Requests:
      'user': get_user,
      'artist': get_artist,
      'track': get_track,
      'recent_tracks': get_recent_tracks,
      'tags': get_tags,
      'user_pool': user_pool
    '''
    password_hash = pylast.md5(AUTH_DATA['password'])

    self.network = pylast.LastFMNetwork(
        api_key=AUTH_DATA['API_KEY'],
        api_secret=AUTH_DATA['API_SECRET'],
        username=AUTH_DATA['username'],
        password_hash=password_hash
    )

  # utility
  def timestamp_x_days_ago(self, n_days):
    """ Returns (int) timestamp from X days ago from now.
    """
    d = date.today() - timedelta(days=n_days)
    dt = datetime(
            year=d.year,
            month=d.month,
            day=d.day
        )
    return int(dt.timestamp())  

  def get(self, request=None, *args, **kwargs): 
    ''' Query on the network and return the result on file.
    
    Args: 
      request to be carried out and its arguments
    Return: 
      path containing the result
    '''
    # utility
    def give_id(some_string):
      """ Returns hashed (sha1) string to be used as ID.
      """
      key = hashlib.sha1()
      key.update(some_string.encode('utf-8'))
      return key.hexdigest()

    # LastFM
    def get_tags(some_obj):
      """ Returns a dict of the top tags set by users to this object.
      """ 
      tag = {tag.item.name for tag in some_obj.get_top_tags(limit=TAG_LIMIT)}
      tag = {t:give_id(t) for t in tag}
      return tag

    def get_user(user_name):
      """ Returns User dict.
      """
      if not isinstance(user_name, pylast.User):
        user = self.network.get_user(user_name)
      else: user = user_name

      try: country = user.get_country().name 
      except: country = None

      try: playcount = user.get_playcount()
      except: playcount = None

      try: reg_date = user.get_registered()
      except: reg_date = None

      try: url = user.get_url()
      except: url = None

      d = {
        'user' : user.name,
        'playcount': playcount,
        'reg_date' : reg_date,
        'country' : country,
        'url' : url
      }
      d['id'] = give_id(d['user']) 
      return d

    def get_artist(artist_name):
      """ Returns Artist dict.
      """
      artist = self.network.get_artist(artist_name)

      try: bio = artist.get_bio("summary")
      except: bio = None

      try: url = artist.get_url()
      except: url = None

      d = {
        'artist' : artist.name,
        'bio' : bio,
        'url' : url
      }
      d['id'] = give_id(d['artist']) 
      return d

    def get_track(artist, title):
      """ Returns Track dict.
      """
      try: track = self.network.get_track(artist,title)
      except: 
        print('Track not found')
        d = {
        'artist' : artist,
        'title': title,
        'not found': True
        }
        return d 

      try: album = track.get_album().title
      except: album = None

      try: duration = track.get_duration()
      except: duration = None 

      try: url = track.get_url()
      except: url = None

      try: tags = get_tags(track)
      except: tags = None

      d = {
        'artist' : track.artist.name,
        'title': track.title,
        'album': album,
        'duration': duration,
        'tags': tags,
        'url': url
      }
      d['id'] = give_id(d['artist']+d['title']) 
      return d

    def get_playedtrack(playedtrack):
      """ Returns PlayedTrack dict.
      """
      d = {
        'artist':playedtrack.track.artist.name,
        'title':playedtrack.track.title, 
        'date':playedtrack.playback_date,
        'album': playedtrack.album,
        'timestamp': playedtrack.timestamp
      }
      d['id'] = give_id(d['artist']+d['title'])
      return d

    def get_recent_tracks(
      user_name, limit=10, cacheable=True, stream=False,
      time_from=None, time_to=None, now_playing=False
    ):
      """ Get a dict of this user's recent tracks. 
      """
      user = self.network.get_user(user_name)
      recent = user.get_recent_tracks( 
        limit=limit, cacheable=cacheable, stream=stream, 
        time_from=time_from, time_to=time_to, now_playing=now_playing
      )
      d = []
      d.append(user_name)
      for track in recent:
        d.append(get_playedtrack(track)) 
      return d

    def user_pool(user_name, MAX=20):
      """ Returns friends and friends of friends of seed user until len(user_pool) gets to MAX.
      """
      user = self.network.get_user(user_name)
      def get_friend(theuser):
          for friend in theuser.get_friends(limit=100):
              if len(get_friend.user_pool) < MAX and friend not in get_friend.user_pool:
                fr = get_user(friend)
                get_friend.user_pool.append(fr)
          if len(get_friend.user_pool) < MAX:
              get_friend.index += 1
              get_friend(get_friend.user_pool[index])
      get_friend.user_pool = []
      get_friend.index = 0
      get_friend(user)
      return get_friend.user_pool

    requests_dict = { 
        'user': get_user,
        'artist': get_artist,
        'track': get_track,
        'recent_tracks': get_recent_tracks,
        'tags': get_tags,
        'user_pool': user_pool
    }

    result = requests_dict[request](*args, **kwargs)
    return result


