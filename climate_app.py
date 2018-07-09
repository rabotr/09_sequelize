# ## Step 4 - Climate App

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# * Use FLASK to create your routes.
from datetime import datetime
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Homework/Instructions/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurements = Base.classes.Measurement
Stations = Base.classes.Station

# Create session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2018-01-01<br/>" 
        f"/api/v1.0/2017-01-01/2018-01-01<br/>" 
    )

# * `/api/v1.0/precipitation`
###   * Query for the dates and temperature observations from the last year.
###   * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
###   * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """dates and temperature observations from the last year"""
    # Query all passengers
    sel = [Measurements.date, Measurements.prcp]
    results = session.query(*sel).\
        filter(Measurements.date.between('2016-08-23','2017-08-23')).all()

    # Convert into dict
    precip_results = []
    for r in results:
        precip_dict = {}
        precip_dict["Date"] = r.date
        precip_dict["Precipitation"] = r.prcp
        precip_results.append(precip_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precip_results)

# * `/api/v1.0/stations`
###   * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    # Query
    sel = [Stations.name, Measurements.station]
    station_query = session.query(*sel).\
        filter(Measurements.station == Stations.station).\
        group_by(Stations.name).\
        order_by(func.count(Measurements.station).desc()).all()

    # Convert into dict
    station_results = []
    for s in station_query:
        station_dict = {}
        station_dict["Name"] = s.name
        station_dict["Station"] = s.station
        station_results.append(station_dict)

    return jsonify(station_results)

# * `/api/v1.0/tobs`
###   * Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    # Query
    sel = [Measurements.date, Measurements.tobs]
       
    tobs_query = session.query(*sel).\
        filter(Measurements.date.between('2016-08-23','2017-08-23')).all()
    
    # Convert into dict
    tobs_results = []
    for t in tobs_query:
        tobs_dict = {}
        tobs_dict["Date"] = t.date
        tobs_dict["Temp"] = t.tobs
        tobs_results.append(tobs_dict)

    return jsonify(tobs_results)

# * `/api/v1.0/<start>`
###   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
###   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    """temp data by start date"""

    import pdb; pdb.set_trace()
    start = datetime.strptime(start, "%Y-%m-%d").date()

    # Query
    sel = [Measurements.date, Measurements.tobs]
       
    start_results = session.query(*sel, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date.between(start, Measurements.date.max())).all()

    return jsonify(start_results)

# # `/api/v1.0/<start>/<end>`
# ###   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# ###   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """temp data by start and end date"""
    # start = datetime.strptime(start, "%Y-%m-%d").date()
    # end = datetime.strptime(end, "%Y-%m-%d").date()

    # Query
    sel = [Measurements.date, Measurements.tobs]
    import pdb; pdb.set_trace()
    start_end_results = session.query(Measurements.date, Measurements.tobs, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date > start).filter(Measurements.date < end).all()

    return jsonify(start_end_results)

if __name__ == '__main__':
    app.run(debug=True)




