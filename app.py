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
    return (
        "API Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date<br/>"
        "/api/v1.0/start_date/end_date<br/>"
        "IMPORTANT TIP: Put the start_date and end_date in 'YYYY-MM-DD' format<br/>"
        )
















if __name__ == "__main__":
    app.run(debug=True)
