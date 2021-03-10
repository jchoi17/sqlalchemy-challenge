  
#################################################
# Import Dependencies
#################################################
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


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
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/[start format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]/[end format:yyyy-mm-dd]<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

    session.close()


   
    
    # Convert the list to Dictionary
    prcp_list = []
    for date,prcp  in results:
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

    for x in station:
        station_list.append(temp_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/<start>")
def temp_query():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    #return results
    temp_list = []

    for min,avg,max in queryresult:
        temp_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(temp_dict)

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_query():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    #return results
    se_temp = []

    for min,avg,max in queryresult:
        se_dict = {}
        se_dict["Min"] = min
        se_dict["Average"] = avg
        se_dict["Max"] = max
        se_temp.append(se_dict)

    return jsonify(se_temp)


if __name__ == '__main__':
    app.run(debug=True)