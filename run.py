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
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html', 
    ingredients=mongo.db.ingredients.find(), 
    ingredients2=mongo.db.ingredients.find(), 
    categories=mongo.db.categories.find())
    

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            