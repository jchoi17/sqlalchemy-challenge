  
#################################################
# Import Dependencies
#################################################
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../DataClass/Homework/10-Advanced-Data-Storage-and-Retrieval/sqlalchemy-challenge/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[start]/[end]<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    x = dt.datetime(2016, 8, 23)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= x).all()

    session.close()
   
    
    # Convert the list to Dictionary
    prcp_list = []
    for date, prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).order_by(Station.station).all()

    session.close()

    #return results
    station_list = []

    for s in results:
        station_list.append(s)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_query():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    x = dt.datetime(2016, 8, 23)

    """Return a list of all passenger names"""
    # Query all passengers
    result = session.query(Measurement.tobs).filter(Measurement.date >= x, Measurement.station == "USC00519281").all()

    session.close()

    #return results
    temp_list = []

    for r in result:
        temp_list.append(r)
    
    return jsonify(temp_list)



@app.route("/api/v1.0/<start>")
def start_temp(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    #return results
    start_temp = []

    for min,avg,max in result:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Average"] = avg
        start_dict["Max"] = max
        start_temp.append(start_dict)

    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def se_temp(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    session.close()

    #return results
    se_temp = []

    for min,avg,max in result:
        se_dict = {}
        se_dict["Min"] = min
        se_dict["Average"] = avg
        se_dict["Max"] = max
        se_temp.append(se_dict)

    return jsonify(se_temp)


if __name__ == '__main__':
    app.run(debug=True)