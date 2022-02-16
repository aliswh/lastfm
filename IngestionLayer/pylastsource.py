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
      f = open(f"data/{request+timestamp}", 'w', encoding="utf-8") # TODO: should name include something else?
      f.write(result.__repr__()) # TODO: write to GCS, to json?
      f.close()

    def get_user(user_name):
      """ Return User object.
      """
      return self.network.get_user(user_name)

    def get_artist(artist_name):
      return self.network.get_artist(artist_name)

    def get_track(artist, title):
      """ Return Track object.
      """
      return self.network.get_track(artist,title)

    def get_recent_tracks(user, 
      limit=10, cacheable=True, stream=False,
      time_from=None, time_to=None, now_playing=False
    ):
      """ Get a list of this user's recent tracks.
      """
      return user.get_recent_tracks(
        limit=limit, cacheable=cacheable, stream=stream, 
        time_from=time_from, time_to=time_to, now_playing=now_playing
      )

    def get_tags(self):
      """ Returns a list of the tags set by the user to this object."""
      return self.get_tags()

    requests_dict = {
        'user': get_user,
        'artist': get_artist,
        'track': get_track,
        'recent_tracks': get_recent_tracks,
        'tags': get_tags
    }

    result = requests_dict[request](*args, **kwargs)
    if save_file: save_result(request, result)
    return result


