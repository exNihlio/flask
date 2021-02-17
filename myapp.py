#!/usr/bin/env python3

import logging as log
from socket import gethostname
from flask import Flask, render_template
from os import environ as env
from flask import jsonify
from pymemcache.client.base import Client as mClient
from redis import Redis as r
app = Flask(__name__)

@app.route('/')
def index():
    turtles = "static/images/tur_in_shell_resize.png"
    hostname = gethostname()
    bg_color = 'AliceBlue;'
    try:
        redisURL = env['redisURL']
    except:
        redisURL = 'localhost'
        log.warning('Warning: Set redisURL to: {}'.format(redisURL))

    try:
        redisPort = env['redisPort']
    except:
        redisPort = 6379

    # redis client
    rClient = r(host=redisURL, port=redisPort)
    try:
        rClient.incr('website:hits')
        rCount = rClient.get('website:hits')
    except:
        log.warning('Unable to retrieve website hits from Redis')
        rCount = 'Unknown'

    if rCount == 'Unknown':
        pass
    else:
        try:
            rCount = int(rCount.decode('utf-8'))
        except:
            log.warning('Error decoding hits')
            rCount = 'Unable to decode hits from Redis'

    # Rendered HTML
    return render_template('index.html', hostname=hostname, bg_color=bg_color, 
                            redis_count=rCount, img_src=turtles)

#@app.route('/db')
#def dbStatus():
#    try:
#        env['POSTGRES_PASSWORD']
#        db_color = 'background-color:MediumSeaGreen;'
#    except:
#        db_color = 'background-color:Tomato;'
#
#    # Remains red until we can try database access
#    db_access_color= 'background-color:Tomato;'
#
#    try:
#        env['AVLOG_RDS_ENDPOINT']
#        avlog_rds_color = 'background-color:MediumSeaGreen;'
#    except:
#        avlog_rds_color = 'background-color:Tomato;'
#        
#    return render_template('db.html', avlog_rds_color=avlog_rds_color,
#                                      db_color=db_color,
#                                      db_access_color=db_access_color)
#