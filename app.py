import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db

load_dotenv()

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=8000, debug=True)