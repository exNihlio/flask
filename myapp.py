#!/usr/bin/env python3

import logging
from socket import gethostname
from flask import Flask, render_template
from os import environ as env
from flask import jsonify
from pymemcache.client.base import Client as mClient
app = Flask(__name__)

@app.route("/")
def index():
    hostname = gethostname()
    bg_color = "AliceBlue;"
    try:
        memcachedURL = env['memcachedURL']
    except:
        memcachedURL = 'localhost' 
        log.warning("Warning: Set memcachedURL to: {}".format(memcachedURL))

    # memcached client
    c = mClient((memcachedURL, 11211))
    try: 
        int_count = c.get('count')
    except:
        int_count = 'Error retrieving results'

    if int_count == None:
        c.set('count', 0)
        
    try:
        c.incr('count', 1)
    except:
        pass

    try:
        int_count = int(int_count.decode('utf-8'))
    except:
        pass

    return render_template("index.html", hostname=hostname, bg_color=bg_color, count=int_count)

@app.route("/db")
def dbStatus():
    try:
        env['POSTGRES_PASSWORD']
        db_color = "background-color:MediumSeaGreen;"
    except:
        db_color = "background-color:Tomato;"

    # Remains red until we can try database access
    db_access_color= "background-color:Tomato;"

    try:
        env['AVLOG_RDS_ENDPOINT']
        avlog_rds_color = "background-color:MediumSeaGreen;"
    except:
        avlog_rds_color = "background-color:Tomato;"
        
    return render_template("db.html", avlog_rds_color=avlog_rds_color,
                                      db_color=db_color,
                                      db_access_color=db_access_color)

@app.route("/endpoint")
def ecrStatus():
    try:
        env['ECR_ENDPOINT'] 
        endpoint_color = "background-color:MediumSeaGreen;"
    except:
        endpoint_color = "background-color:Tomato;"
    
    return render_template("endpoint.html", endpoint_color=endpoint_color)

if __name__ == "__main__":
    app.run()

@app.route("/json")
def basic():
    people = [ 
                {
                    "name": "Nicole",
                    "age": 23
                },
                {
                    "name": "Claire",
                    "age": 27,
                }
            ]
              
               
    return jsonify(people)

@app.route('/memcache')
def webCount():
    return website_count
