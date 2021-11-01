from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from pymongo.common import MAX_SUPPORTED_WIRE_VERSION
import scraping

# app name set up
app = Flask(__name__)

# connection to PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run()