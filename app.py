import os

import pymongo as pymongo
from bson import ObjectId
from flask import Flask, render_template, request, flash, redirect, url_for

# Set environmental variables
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
CLUSTER = os.getenv("CLUSTER")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Create database connection and naming the database and collection
client = pymongo.MongoClient(
    "mongodb+srv://" + USERNAME + ":" + PASSWORD + "@" + CLUSTER + ".mongodb.net/test?retryWrites=true&w=majority")
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app = Flask(__name__)

# Set the cache to 0 -> There is no cache at all
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get('SECRET_KEY')


def collect_data():
    """Fetch all the data from the database"""
    book_array = []

    for books in collection.find():
        book_array.append(books)

    ordered_book_array = book_array[::-1]

    return ordered_book_array


def collect_data_update(item_id):
    """Fetched the picked books data from the database"""
    return collection.find({"_id": ObjectId(item_id)})


@app.route('/')
def index():
    return render_template('base.html', books=collect_data())


@app.route('/fantasy')
def fantasy():
    return render_template('fantasy.html', books=collect_data())


@app.route('/horror')
def horror():
    return render_template('horror.html', books=collect_data())


@app.route('/thriller')
def thriller():
    return render_template('thriller.html', books=collect_data())


@app.route('/recommendation')
def recommendation():
    return render_template('recommend.html')


@app.route('/create', methods=["POST"])
def create():
    """Create a new object in the database"""
    author = request.form["author"]
    book_title = request.form["book_title"]
    genre = request.form["genre"]
    recommendation = request.form["recommendation"]
    book_cover_pic = request.form["book_cover_pic"]

    if len(str(author)) == 0 or len(str(book_title)) == 0 or len(str(book_cover_pic)) == 0:
        flash("One of the input field is empty, please fill out all the required fields!")
        return redirect(url_for("recommendation"))

    if genre != "Fantasy" or genre != "Horror" or genre != "Thriller":
        flash("Wrong genre type!")
        return redirect(url_for("recommendation"))

    if len(str(recommendation)) > 301:
        flash("You wrote too long recommendation")
        return redirect(url_for("recommendation"))



    mydict = {
        "author": author,
        "title": book_title,
        "genre": genre,
        "cover_picture_link": book_cover_pic,
        "recommendation": recommendation}

    collection.insert_one(mydict)

    flash("You have been created a new book recommendation!")
    return redirect(url_for("index"))


@app.route('/update/<item_id>')
def fill_out_update(item_id):
    """Gives you back the update form with the details of the picked book"""
    id = collect_data_update(item_id)
    return render_template('update.html', book=id)


@app.route('/update/<id>', methods=["POST"])
def update(id):
    """Update the details of the picked book"""
    author = request.form["author"]
    book_title = request.form["book_title"]
    genre = request.form["genre"]
    recommendation = request.form["recommendation"]
    book_cover_pic = request.form["book_cover_pic"]

    if len(str(author)) == 0 or len(str(book_title)) == 0 or len(str(book_cover_pic)) == 0:
        flash("One of the input field is empty, please fill out all the required fields!")
        return redirect(url_for("recommendation"))

    if genre != "Fantasy" or genre != "Horror" or genre != "Thriller":
        flash("Wrong genre type!")
        return redirect(url_for("recommendation"))

    if len(str(recommendation)) > 301:
        flash("You wrote too long recommendation")
        return render_template('update.html', book=collect_data_update(id))

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

    flash("You have been updated a new book recommendation!")

    return redirect(url_for("index"))


@app.route('/delete/<item_id>')
def delete(item_id):
    """Delete chosen book from the page"""
    collection.delete_one(
        {"_id": ObjectId(item_id)},
    )

    flash("You have been deleted the chosen book!")

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
