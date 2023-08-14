# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# Declare a Base using 'automap_base'
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
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
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return last 12 months of precipitation data"""

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date, 
           func.max(measurement.prcp)]
    historical_prcp = session.query(*sel).\
        group_by(measurement.date).\
        filter(measurement.date>= "2016-08-23").all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    precip = []
    for date, prcp in historical_prcp:
        precip_dict = {
            "date": date,
            "prcp": prcp
        }
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of stations"""
    # Query all stations
    stations = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def most_active():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return last 12 months of temperature observations from the most active station"""
    
    sel = [measurement.date, measurement.tobs]
    historical_tobs = session.query(*sel)\
        .filter(measurement.date>= "2016-08-23")\
        .filter(measurement.station== "USC00519281")\
        .all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of temperature observations
    tobs = []
    for date, tobs_value in historical_tobs:
        tobs_dict = {
            "date": date,
            "tobs": tobs_value
        }
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def tobs_after_start(start):
    """Return min, max, average temperature observations (tobs) after a given start date"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform query to return list of the minimum temperature, the average temperature, and the maximum temperature for specified start range
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    tobs_after_start = session.query(*sel)\
        .filter(measurement.date >= start)\
        .all()
    
    session.close()

    tobs = list(np.ravel(tobs_after_start))
    
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def tobs_between(start, end):
    """Return min, max, average temperature observations (tobs) between a given start and end date"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform query to return list of the minimum temperature, the average temperature, and the maximum temperature for specified start range
    sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    tobs_between = session.query(*sel)\
        .filter(measurement.date >= start)\
        .filter(measurement.date <= end)\
        .all()
    
    session.close()

    tobs = list(np.ravel(tobs_between))
    
    return jsonify(tobs)

if __name__ == '__main__':
    app.run(debug=True)


