#!pip install requests # TODO
#!pip install pylast

import requests
import json
import pylast
import time
from abstract_ingestion_layer import Source

class PyLastSource(Source):
  def __init__(self, AUTH_DATA:dict):
    ''' Initialization of 'Network' object from PyLast.
    
    Args: dictionary w/ all authentication data, which includes:
      -  API_KEY,
      -  API_SECRET,
      -  username,
      -  password
    '''
    password_hash = pylast.md5(AUTH_DATA['password'])

    self.network = pylast.LastFMNetwork(
        api_key=AUTH_DATA['API_KEY'],
        api_secret=AUTH_DATA['API_SECRET'],
        username=AUTH_DATA['username'],
        password_hash=password_hash
    )

  def get(self, request=None, *args, **kwargs): 
    ''' Query on the network and return the result on file.
    
    Args: 
      request to be carried out and its arguments
    Return: 
      path containing the result
    '''
    def save_result(request_name, result, info=''):
      """ Save request result in a file with timestamp.
      """
      #timestamp = time.strftime("%Y%m%d-%H%M%S") #TODO serve?
      filename = f"{info+request+str(result['id'])}.json"
      f = open(filename, 'w', encoding="utf-8")
      f.write(json.dumps(result))
      f.close()

    def give_id(some_string):
      return hash(some_string)

    def get_user(user_name):
      user = self.network.get_user(user_name)
      d = {
        'user' : user.name,
      }
      d['id'] = give_id(d['user']) 
      return d

    def get_artist(artist_name):
      artist = self.network.get_artist(artist_name)
      d = {
        'artist' : artist.name,
      }
      d['id'] = give_id(d['artist']) 
      return d

    def get_track(artist, title):
      track = self.network.get_track(artist,title)
      d = {
        'artist' : track.artist.name,
        'title': track.title,
      }
      d['id'] = give_id(d['artist']+d['title']) 
      return d

    def get_tags(self):
      """ Returns a list of the tags set by the user to this object.""" # TODO
      return self.get_tags()

    def get_playedtrack(playedtrack):
      """ Return PlayedTrack dict.
      """
      d = {
        'track':str(playedtrack.track), # TODO
        'date':playedtrack.playback_date,
        'album': playedtrack.album,
        'timestamp': playedtrack.timestamp
      }
      return d

    def get_recent_tracks(
      user, limit=10, cacheable=True, stream=False,
      time_from=None, time_to=None, now_playing=False
    ):
      """ Get a list of this user's recent tracks.
      """
      recent = user.get_recent_tracks(
        limit=limit, cacheable=cacheable, stream=stream, 
        time_from=time_from, time_to=time_to, now_playing=now_playing
      )
      d = {}
      for i,track in enumerate(recent):
        d[i] = get_playedtrack(track)
      d['id'] = give_id(str(user)) # TODO
      return d

    requests_dict = { 
        'user': get_user,
        'artist': get_artist,
        'track': get_track,
        'recent_tracks': get_recent_tracks,
        'tags': get_tags
    }

    result = requests_dict[request](*args, **kwargs)
    info = str(args[0])+'-' if request == 'recent_tracks' else ''
    save_result(request, result, info)
    return result


