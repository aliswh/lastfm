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

  def get(self, request=None, save_file=False, *args, **kwargs): 
    ''' Query on the network and return the result on file.
    
    Args: 
      request to be carried out and its arguments
    Return: 
      path containing the result
    '''
    def save_result(request_name, result):
      """ Save request result in a file with timestamp.
      """
      timestamp = time.strftime("%Y%m%d-%H%M%S")
      f = open(f"{request+timestamp}.json", 'w', encoding="utf-8") # TODO: include username in recent tracks
      f.write(json.dumps(result)) 
      f.close()

    def get_user(user_name):
      return self.network.get_user(user_name)

    def get_artist(artist_name):
      return self.network.get_artist(artist_name)    

    def get_track(artist, title):
      return self.network.get_track(artist,title)

    def get_tags(self):
      """ Returns a list of the tags set by the user to this object."""
      return self.get_tags()

    def get_track_json(playedtrack):
      """ Return PlayedTrack json.
      """
      date = playedtrack.playback_date # TODO better format

      d = {
        'artist':playedtrack.track.artist.name, # delete name to get obj Artist
        'title':playedtrack.track.title,
        'duration':playedtrack.track.get_duration(),
        'album': playedtrack.album,
        'timestamp': playedtrack.timestamp
      }
      return date, d

    def get_recent_tracks(user, 
      limit=10, cacheable=True, stream=False,
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
        key, value = get_track_json(track)
        d[key] = value
      return d

    requests_dict = { # TODO: is this necessary? have only one possible request
        'user': get_user,
        'artist': get_artist,
        'track': get_track,
        'recent_tracks': get_recent_tracks,
        'tags': get_tags
    }

    result = requests_dict[request](*args, **kwargs)
    if save_file: save_result(request, result)
    return result


