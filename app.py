#Import Dependencies
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect existing database into model
Base = automap_base()
Base.prepare(engine, reflect=True)

#Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (f"Available Routes:<br/>"\

            f"/api/v1.0/precipitation"\

            f"/api/v1.0/stations"\

            f"/api/v1.0/tobs"\

            f"/api/v1.0/start"\

            f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    #Create Session
    session = Session(engine)

    #Query precipitation data ordered by date
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date)
    
    #Close session
    session.close()

    #Create dictionary from row data and append to library
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)
    
    #return results in json format
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    #Create Session
    session = Session(engine)
    
    #Query all station names
    stations = session.query(station.name).all()
    
    #Create list with queried info
    station_list = list(np.ravel(stations))

    session.close()

    #return stations in json format
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    #Create Session
    session = Session(engine)
    
    #Find only data within the last year
    year_before = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #Query temperature observations within one year at the most active station.
    tobs_data = session.query(measurement.date, measurement.tobs)\
                .filter(measurement.station == 'USC00519281')\
                .filter(measurement.date >= year_before).all()
    
    #Create list with queried info
    tobs_list = list(np.ravel(tobs_data))

    session.close()

    #return data in json format
    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def start(start):
    
    #Create session
    session = Session(engine)
    
    #Query temperature observations to find min, max and avg temp. for all dates greater than or equal to the start date.
    start_data = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),                func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date)                .all()
    
    #Create list with queried info
    start_list = list(np.ravel(start_data))

    session.close()

    #return data in json format
    return jsonify(start_list)

@app.route("/api/v1.0/start/end")
def start_end(start, end):

    #Create session
    session = Session(engine)

        #Query temperature observations to find min, max and avg temp. for dates between start and end
    start_end = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).group_by(measurement.date).all()

    #Create list with queried info
    start_end_list = list(np.ravel(start_end))

    session.close()
    
    #return data in json format
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)

