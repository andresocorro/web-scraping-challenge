from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__, template_folder='templates')

#Using pymongo to setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    mars_page = mongo.db.mars_page.find_one()
    return render_template("index.html", mars_page = mars_page)

@app.route("/scrape")

def scrape():
    mars_page = mongo.db.mars_page
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.scrape_img()
    mars_data = scrape_mars.scrape_facts()
    mars_data = scrape_mars.scrape_hemisphere()
    mars_page.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug= True)

