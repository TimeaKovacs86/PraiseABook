import os

import pymongo as pymongo
from flask import Flask, render_template

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CLUSTER = os.getenv("CLUSTER")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = pymongo.MongoClient(
    "mongodb+srv://" + USERNAME + ":" + PASSWORD + "@" + CLUSTER + ".mongodb.net/test?retryWrites=true&w=majority")

app = Flask(__name__)


@app.route('/')
def index():
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    x = collection.find_one()

    return render_template('base.html')


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
