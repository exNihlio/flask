#!/usr/bin/env python3

from socket import gethostname
from flask import Flask, render_template
from os import environ as env
from flask import jsonify
app = Flask(__name__)

@app.route("/")
def index():
    hostname = gethostname()
    bg_color = "AliceBlue;"

    return render_template("index.html", hostname=hostname, bg_color=bg_color)

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
