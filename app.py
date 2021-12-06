import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurement dates and precipitation"""
   
    result = session.query(measurement.date, measurement.prcp).all()
    prcp_df = pd.DataFrame(result)
    last_year_df = prcp_df.tail(365)


    # Sort the dataframe by date
    new_column_list = ['Date', 'Precipitation']
    last_year_df= last_year_df.set_axis(new_column_list, axis=1)

    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(last_year_df))

    return jsonify(data)

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    station_name = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(station_name))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    sel = [measurement.station, measurement.date, measurement.prcp, measurement.tobs, station.name]
    stations = session.query(*sel).filter(measurement.station == station.station).all()
    
    session.close()
    

    data = pd.DataFrame(stations)
    data.sort_values([0], ascending=[False])
    result = list(np.ravel(data))

    return jsonify(result)

    

@app.route("/api/v1.0/<start>")
def date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    
    sel = [measurement.station, measurement.date, measurement.prcp, measurement.tobs, station.name]
    stations = session.query(*sel).filter(measurement.station == station.station).all()


    result = session.query(measurement.date > start).all()
    session.close()

  
    results = list(np.ravel(result))
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    sel = [measurement.station, measurement.date, measurement.prcp, measurement.tobs, station.name]
    stations = session.query(*sel).filter(measurement.station == station.station).all()


    result = session.query(measurement.date > start and measurement.date < end).all()
    session.close()

  
    results = list(np.ravel(result))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)





