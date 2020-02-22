# 1. import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# 2. Database setup
engine=create_engine("sqlite:///Resources/hawaii.sqlite")
# relfect an existing database into a new model
Base=automap_base()
Base.prepare(engine,reflect=True)
# 3. save reference to the table
Measurement=Base.classes.measurement
Station = Base.classes.station
# 4. Create an app, being sure to pass __name__
app = Flask(__name__)

# 5. Create flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Climate API!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"-the dates and precipitation observations from 2016-08-23 to 2017-08-23<br/>"
        f"/api/v1.0/stations<br/>"
        f"-the station list from database<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-the dates and temperature observations from last 12 months<br/>"
        f"/api/v1.0/2015-03-15<br/>"
        f"-the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to 2015-03-15<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23<br/>"
        f"-the minimum temperature, the average temperature, and the max temperature for dates between 2016-08-23 and 2017-08-23 inclusive"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >"2016-08-22").\
        filter(Measurement.date<"2017-08-24").all()
    
    session.close()

    all_precipitation=[]
    for date,prcp in results:
        precipitation_dict={"date":"prcp"}
        precipitation_dict["date"]=date
        precipitation_dict["prcp"]=prcp
        all_precipitation.append(precipitation_dict)
    
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def station():
    session=Session(engine)
    results=session.query(Station.station,Station.name).all()

    session.close()

    all_station=[]
    for station,name in results:
        station_dict={"station":"name"}
        station_dict["station"]=station
        station_dict["name"]=name
        all_station.append(station_dict)

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tob():
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >"2016-08-22").\
        filter(Measurement.date<"2017-08-24").all()
    
    session.close()

    all_tob=[]
    for date,tob in results:
        tob_dict={"date":"tob"}
        tob_dict["date"]=date
        tob_dict["tobs"]=tob
        all_tob.append(tob_dict)
    
    return jsonify(all_tob)

@app.route("/api/v1.0/2015-03-15")
def start():
    session=Session(engine)
    results = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= "2015-03-15").all()
    
    session.close()
    start_temp=[]
    for min_tob,avg_tob,max_tob in results:
        start_temp_dict={}
        start_temp_dict["Minium_Temperature"]=min_tob
        start_temp_dict["Average_Temperature"]=avg_tob
        start_temp_dict["Max_Temperature"]=max_tob
        start_temp.append(start_temp_dict)
    
    return jsonify(start_temp)

@app.route("/api/v1.0/2016-08-23/2017-08-23")
def start_end():
    session=Session(engine)
    results = session.query(func.max(Measurement.tobs), \
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= "2016-08-23").\
                            filter(Measurement.date<="2017-08-23") .all()
    
    session.close()
    start_end_temp=[]
    for min_tob,avg_tob,max_tob in results:
        start_end_temp_dict={}
        start_end_temp_dict["Minium_Temperature"]=min_tob
        start_end_temp_dict["Average_Temperature"]=avg_tob
        start_end_temp_dict["Max_Temperature"]=max_tob
        start_end_temp.append(start_end_temp_dict)
    
    return jsonify(start_end_temp)

if __name__ == '__main__':
    app.run(debug=True)


