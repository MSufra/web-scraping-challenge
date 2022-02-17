#import libraries
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import scrape
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#default page
@app.route("/")
def home():

    # Find data from the mongo database
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars_data= mars_data)

#call scrape
@app.route("/scrape")
def scraper():
    app_data = scrape.scrape()

    mongo.db.collection.update_one({}, {"$set": app_data}, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
