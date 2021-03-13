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
    session.close()
    # Using code from the query from Part 1.
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    #
    last_year = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = dt.date(last_year.year, last_year.month, last_year.day) - dt.timedelta(days=365)
    












if __name__ == "__main__":
    app.run(debug=True)
