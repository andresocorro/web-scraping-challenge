from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)

#Using pymongo to setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_page
mongo = PyMongo(app)


page = mongo.db.mars_page
page.drop()

@app.route("/")
def index():
    mars_results = mars_page.find()
    return render_template("index.html", mars_results = mars_results)

@app.route("/scrape")

def scraper():
    mars_page = mongo.db.mars_page
    mars_data = scrape_mars.scrape()
    mars_page.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug= True)

