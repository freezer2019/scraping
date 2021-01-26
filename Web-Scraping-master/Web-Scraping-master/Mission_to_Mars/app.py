from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask app
app = Flask(__name__)

# Create a connection to MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)

# Create a route that renders index.html template

@app.route("/")
def index():
    mars_data = mongo.db.mars_scrapedit.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():

    mars_scrapedit = mongo.db.mars_scrapedit
    mars_data = scrape_mars.scrape()
    mongo.db.mars_scrapedit.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)