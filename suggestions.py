#!/usr/bin/env python
import ast
import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
import spotipy
import json
import joblib
from spotipy.oauth2 import SpotifyClientCredentials
from credentialSpoty import *  #here you would need to create your own .py file with your Spotify credentials to access the Spotify API
from fuzzywuzzy import fuzz
import Levenshtein as lev
import sklearn
import logging as log

# Configure log level
log.basicConfig(level=log.INFO)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= Client_ID,
                                                           client_secret= Client_Secret))

def load_model_from_file(file_name = 'clustering_model_4.sav'):
    log.info("loading model")
    return joblib.load(open(file_name, 'rb'))

model = load_model_from_file()

def get_song_id(song_name):
    song_info = sp.search(q = song_name, limit = 1)
    song_id = song_info['tracks']['items'][0]['uri']
   
    return(song_id) 

def get_audio_features(song_id):
    features_json = sp.audio_features(song_id) 
    
    energy = features_json[0]['energy']
    instrumentalness = features_json[0]['instrumentalness']
    speechiness = features_json[0]['speechiness']
    valence = features_json[0]['valence']
     
    features_array = [[energy, instrumentalness, speechiness, valence]]
    return (features_array)

def predict_cluster(model, song_features):
    return int(model.predict(song_features))

def read_full_dataset_with_clusters():
    return pd.read_csv('full_data_with_clusters.csv')

def get_random_song_from_cluster(song_cluster):
    file = read_full_dataset_with_clusters()
    songs_in_given_cluster = file[file["cluster"] == song_cluster]
    row = songs_in_given_cluster.sample(n=1).iloc[0]
    list_of_artists = ast.literal_eval(row['artists'])
    song_string = f"{row['name']} by {', '.join(list_of_artists)}"
    return song_string

def recommend_song_from_kaggle_dataset(song_name):
    song_id = get_song_id(song_name)
    audio_features = get_audio_features(song_id)
    predicted_cluster = predict_cluster(model, audio_features)
    recommended_song = get_random_song_from_cluster(predicted_cluster)
    return recommended_song


def scraping_Billboard(url = 'https://www.billboard.com/charts/hot-100'):
    log.info("getting songs from billboard top 100")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = []
    artist = []
    num_iter = 100
    for i in range(num_iter):
        title.append(soup.find_all('span', "chart-element__information__song text--truncate color--primary")[i].get_text())
        artist.append(soup.find_all('span', "chart-element__information__artist text--truncate color--secondary")[i].get_text())
    BillboardTop100 = pd.DataFrame({
                        "artist":artist,
                       "song":title,
                       "Artist":artist,
                       "Song":title })
    a = BillboardTop100['artist'].str.lower()
    s = BillboardTop100['song'].str.lower()

    BillboardTop100['artist'] = a
    BillboardTop100['song'] = s
    BillboardTop100.index += 1
    log.debug(f"{BillboardTop100}")
    log.info("retrieved fresh list of billboard top 100")
    return BillboardTop100
    


rating_top100 = scraping_Billboard()

def recomended_song(get_song):
    global rating_top100
    song_index = rating_top100.index[rating_top100['song'] == get_song].tolist()
    rec_index = random.randint(1,100)
    rec_song = rating_top100['Song'].values[rec_index]
    rec_index = rating_top100.index[rating_top100['Song'] == rec_song].tolist()
    rec_artist = rating_top100['Artist'].values[rec_index]
    
    rec_song_artist_string = f"{rec_song}   by   {rec_artist[0]}"
    #print(f"So maybe you would also like the song '{rec_song}' by {rec_artist[0]}? (number {int(rec_index[0])} in Hot 100)")
    return [song_index[0], rec_song_artist_string, int(rec_index[0])]


# ACTUAL SUGGESTION GENERATING FUNCTION

def suggestion_function(inputed_song):
    get_song = inputed_song.lower()
    global rating_top100
    list_of_ratios = []
    for i in range(100):
        song_from_top = rating_top100['song'].values[i]
        ratio = lev.ratio(song_from_top, get_song)
        list_of_ratios.append(ratio)
    if max(list_of_ratios) > 0.9:
        index_of_song = list_of_ratios.index(max(list_of_ratios))
        real_song = rating_top100['song'].values[index_of_song]
        return recomended_song(real_song)
    else:
        recommendation_from_outside = recommend_song_from_kaggle_dataset(get_song)
        return recommendation_from_outside

