#10.5.1 Use Flask to create web app

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define index route
@app.route("/")
def index():
   #find the mars collection in our database and assign to mars variable
   mars = mongo.db.mars.find_one()
   #return HTML templae using mars collectionn in MongoDB
   return render_template("index.html", mars=mars)

#define scraping route
@app.route("/scrape")
def scrape():
   #access database
   mars = mongo.db.mars
   #hold data form scraping.py file
   mars_data = scraping.scrape_all()
   #update the database
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #navigate back to index to see content
   return redirect('/', code=302)

#tell it to run!
if __name__ == "__main__":
    app.run()

