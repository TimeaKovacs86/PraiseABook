import os

import pymongo as pymongo
from bson import ObjectId
from flask import Flask, render_template, request

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CLUSTER = os.getenv("CLUSTER")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = pymongo.MongoClient(
    "mongodb+srv://" + USERNAME + ":" + PASSWORD + "@" + CLUSTER + ".mongodb.net/test?retryWrites=true&w=majority")
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app = Flask(__name__)


def collect_data():
    book_array = []

    for books in collection.find():
        book_array.append(books)

    return book_array


def collect_data_update(item_id):
    return collection.find({"_id": ObjectId(item_id)})


@app.route('/')
def index():
    return render_template('base.html', books=collect_data())


@app.route('/recommendation')
def recommendation():
    return render_template('recommend.html')


@app.route('/create', methods=["POST"])
def create():
    """create a new object in the database"""
    author = request.form["author"]
    book_title = request.form["book_title"]
    genre = request.form["genre"]
    recommendation = request.form["recommendation"]
    book_cover_pic = request.form["book_cover_pic"]

    mydict = {
        "author": author,
        "title": book_title,
        "genre": genre,
        "cover_picture_link": book_cover_pic,
        "recommendation": recommendation}

    collection.insert_one(mydict)
    return render_template("base.html", books=collect_data())


@app.route('/update/<item_id>')
def fill_out_update(item_id):
    book = collect_data_update(item_id)
    return render_template('update.html', book=book)


@app.route('/update/<id>', methods=["POST"])
def update(id):
    author = request.form["author"]
    book_title = request.form["book_title"]
    genre = request.form["genre"]
    recommendation = request.form["recommendation"]
    book_cover_pic = request.form["book_cover_pic"]

    mydict = {
        "author": author,
        "title": book_title,
        "genre": genre,
        "cover_picture_link": book_cover_pic,
        "recommendation": recommendation
    }

    collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": mydict
        }
    )

    return render_template("base.html", books=collect_data())


@app.route('/delete/<item_id>')
def delete(item_id):
    collection.delete_one(
        {"_id": ObjectId(item_id)},
    )
    return render_template("base.html", books=collect_data())


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
