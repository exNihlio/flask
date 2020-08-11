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
    hostname = gethostname()
    bg_color = 'AliceBlue;'
    try:
        memcachedURL = env['memcachedURL']
    except:
        memcachedURL = 'localhost' 
        log.warning('Warning: Set memcachedURL to: {}'.format(memcachedURL))

    try:
        memcachedPort = env['memcachedPort']
    except:
        memcachedPort = 11211

    try:
        redisURL = env['redisURL']
    except:
        redisURL = 'localhost'
        log.warning('Warning: Set redisURL to: {}'.format(redisURL))


    try:
        redisPort = env['redisPort']
    except:
        redisPort = 6379

    # memcached client
    c = mClient((memcachedURL, int(memcachedPort)))
    try: 
        mCount = c.get('website:hits')
    except:
        log.warning('Unable to retrieve hits from memcached')
        mCount = 'Unknown'

    if mCount == None:
        c.set('website:hits', 1)

    if mCount == 'Unknown':
        pass
    else:
        try:
            mCount = int(mCount.decode('utf-8'))
        except:
            log.warning('Unable to decode hits from memcached')
            mCount = 'Error decoding hits count'
    try:
        c.incr('website:hits', 1)
    except:
        pass

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
    return render_template('index.html', hostname=hostname, bg_color=bg_color, memcached_count=mCount,
                           redis_count=rCount)

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
#@app.route('/endpoint')
#def ecrStatus():
#    try:
#        env['ECR_ENDPOINT'] 
#        endpoint_color = 'background-color:MediumSeaGreen;'
#    except:
#        endpoint_color = 'background-color:Tomato;'
#    
#    return render_template('endpoint.html', endpoint_color=endpoint_color)
#
#if __name__ == '__main__':
#    app.run()
#
#@app.route('/json')
#def basic():
#    people = [ 
#                {
#                    'name': 'Nicole',
#                    'age': 23
#                },
#                {
#                    'name': 'Claire',
#                    'age': 27,
#                }
#            ]
#              
#               
#    return jsonify(people)
#
#@app.route('/memcache')
#def webCount():
#    return website_count
