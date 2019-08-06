import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
    
app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_db'
app.config['MONGO_URI'] = 'mongodb+srv://root:r00tUser@myfirstcluster-tbkzy.mongodb.net/recipe_db?retryWrites=true&w=majority'

mongo = PyMongo(app) #constructor method

#route decorator is a URL that redirects to a Python function
@app.route('/')
@app.route('/get_recipes')
def get_tasks():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)