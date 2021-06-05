#!/usr/bin/python
# -*- coding: utf-8 -*-

import atexit
from apscheduler.schedulers.blocking import BlockingScheduler

import flask
from suggestions import *


from flask import render_template
from flask import request

import logging as log

# Configure log level
# log.basicConfig(level=log.DEBUG)

# Initialize web server

app = flask.Flask(__name__)
app.config['DEBUG'] = True



def refresh_top100():
    print("updating billboard top 100")
    global rating_top100
    rating_top100 = scraping_Billboard()
    print("successfully updated billboard top 100")
    
sched = BlockingScheduler()
sched.add_job(refresh_top100, 'cron', day_of_week='wed', hour=6, jitter=120)
sched.start()


# This API returns our main HTML page

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# This API returns song suggestions

@app.route('/suggestions', methods=['GET'])
def suggest_song():
    song = request.args.get('song')
    
    log.info(f"getting suggestions for {song}")
    
    get_song = song.lower()
    global rating_top100
    list_of_ratios = []
    for i in range(100):
        song_from_top = rating_top100['song'].values[i]
        ratio = lev.ratio(song_from_top, get_song)
        list_of_ratios.append(ratio)
        log.debug(f"similarity ratio with {song_from_top} - {ratio:.2}")
    if max(list_of_ratios) > 0.9:
        index_of_song = list_of_ratios.index(max(list_of_ratios))
        real_song = rating_top100['song'].values[index_of_song]
        log.info(f"{song} found in billboard top 100 as {real_song} with similarity ratio {max(list_of_ratios):.2}")
        recommendation = recomended_song(real_song)
        new_suggestion = recommendation[1]
        suggestion_rank = recommendation[2]
        song_rank = recommendation[0]
        text1 = f"WOW! YOUR SONG IS NOW #{song_rank} IN BILLBOARD HOT 100! HERE IS ANOTHER ONE FOR YOU - #{suggestion_rank}:"
        return render_template('suggestion.html',
                               suggestion=new_suggestion,
                               suggestion_text=text1)
    else:
        recommendation_from_outside = \
            recommend_song_from_kaggle_dataset(get_song)
        
        text2 = f"WOW! YOU HAVE A FANCY TASTE! HERE IS ANOTHER SONG YOU MAY LIKE:"
        
        return render_template('suggestion.html',
                               suggestion=recommendation_from_outside,
                               suggestion_text=text2)



if __name__ == '__main__':
    app.run(use_reloader=False)
