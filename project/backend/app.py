from flask import Flask, jsonify, request, render_template
from config import config_data as config
from flask_sqlalchemy import SQLAlchemy
import psycopg

DEBUG = False
HOST = "127.0.0.1" if DEBUG else "0.0.0.0"

# Initialize the Flask app
app = Flask(__name__)


##################
# RUN DEV SERVER #
##################
if __name__ == "__main__":
    app.run(HOST, debug=DEBUG)