import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 #to communicate with AWS services
from datetime import datetime

def lambda_handler(event, context):
    # Replace these with your actual credentials
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    # Set up authentication
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    #the page URL of Trending 500 songs daily
    play_list_link = 'https://open.spotify.com/playlist/0PMKjSoU937cvzkHpFJ3hf'
    play_list_url = play_list_link.split('/')[4]
    data = sp.playlist_tracks(play_list_url)
    print(data)


    client = boto3.client('s3')
    file_name = 'spotify_raw_' + str(datetime.now()) + '.json'

    client.put_object(Bucket='spotify-etl-project-ahmed-eraki'
      ,Key= 'raw_data/to_process/' + file_name   #the path where I put the output of lambda code function
      ,Body=json.dumps(data))

    
        