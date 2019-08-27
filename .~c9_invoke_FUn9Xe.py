import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    categories=mongo.db.categories.find())
    

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    recipes = mongo.db.recipes
    recipe_name = request.form.get('recipe_name')
    category_name = request.form.get('category_name')
    ingredient_list = request.form.getlist('ingredient_name')
    recipes.insert_one({
    'recipe_name': recipe_name,
    'category_name': category_name,
    'ingredient_name' : ingredient_list})
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes'))

# recipes.insert_one(request.form.to_dict())
# request.form.getlist('ingredient_name') 

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_ingredients = mongo.db.ingredients.find()
    all_categories = mongo.db.categories.find()
    return render_template('edit_recipe.html', recipe=the_recipe, ingredients=all_ingredients, categories=all_categories)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'category_name':request.form.get('category_name'),
        'ingredient_name': request.form.getlist('ingredient_name')
     })
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes'))
 

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            