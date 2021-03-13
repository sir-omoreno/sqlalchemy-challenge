import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup                                #
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

################################################
# Flask Setup and Routes                       #
################################################

app = Flask(__name__)


@app.route("/")
def main_page():
    """ Simple route with a description of the available pages. """
    return (
        "API Available Routes:<br><br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start_date<br>"
        "/api/v1.0/start_date/end_date<br><br>"
        "IMPORTANT TIP: Put the start_date and end_date in 'YYYY-MM-DD' format<br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Establishing connection to the DB, good practice to close after the using it
    session = Session(engine)

    # Using code from the query from Part 1.
    last_date = session.query(measurement.date).order_by(
        measurement.date.desc()).first()
    #
    last_year = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = dt.date(last_year.year, last_year.month,
                           last_year.day) - dt.timedelta(days=365)
    query_to_retrieve = session.query(measurement.date, func.avg(measurement.prcp)).filter(
        measurement.date >= one_year_ago).group_by(measurement.date).all()

    query_to_retrieve = session.query(measurement.station, measurement.date, measurement.prcp)\
        .filter(measurement.date >= one_year_ago).all()

    session.close()

    list = []
    for i in query_to_retrieve:
        dict = {"Station": i[0], "Date": i[1], "Precipitation": i[2]}
        list.append(dict)
    return jsonify(list)


@app.route("/api/v1.0/stations")
def stations():
    # Establishing connection to the DB, good practice to close after the using it
    session = Session(engine)

    stations = session.query(
        station.station, station.name, station.latitude, station.longitude).all()

    session.close()

    list = []
    for i in stations:
        dict = {"Station ID": i[0], "Station Name": i[1],
                "Station Latitude": i[2], "Station Longitude": i[3]}
        list.append(dict)
    return jsonify(list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(measurement.date).order_by(
        measurement.date.desc()).first()

    last_year = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = dt.date(last_year.year, last_year.month,
                           last_year.day) - dt.timedelta(days=365)

    count = [measurement.station, func.count(measurement.station)]
    active_stations = session.query(*count)\
        .group_by(measurement.station)\
        .order_by(func.count(measurement.station).desc()).all()

    test = [measurement.date, measurement.tobs]
    query_temps = session.query(*test)\
        .filter(measurement.date >= one_year_ago)\
        .filter(measurement.station == active_stations[0][0]).all()

    session.close()

    list = []
    for i in query_temps:
        dict = {"Date": i[0], "Temperature": i[1]}
        list.append(dict)

    return jsonify(list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    query = session.query(func.min(measurement.tobs),
                          func.max(measurement.tobs),
                          func.avg(measurement.tobs))\
        .filter(measurement.date >= start)\
        .order_by(measurement.date.desc()).all()

    session.close()

    for i in query:
        dict = {"Min Temp": i[0], "Max Temp": i[1], "Avg Temp": i[2]}

    return jsonify(dict)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date(start, end):
    session = Session(engine)

    query = session.query(func.min(measurement.tobs),
                          func.max(measurement.tobs),
                          func.avg(measurement.tobs))\
        .filter(measurement.date >= start, measurement.date <= end)\
        .order_by(measurement.date.desc()).all()

    session.close()

    for i in query:
        dict = {"Min Temp": i[0], "Max Temp": i[1], "Avg Temp": i[2]}

    return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True)
