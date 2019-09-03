import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.objectid import ObjectId
    
app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_db'
app.config['MONGO_URI'] = 'mongodb+srv://root:r00tUser@myfirstcluster-tbkzy.mongodb.net/recipe_db?retryWrites=true&w=majority'


mongo = PyMongo(app) #constructor method

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

#route decorator is a URL that redirects to a Python function
@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find(), files=mongo.db.fs.files.find())


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html', ingredients=mongo.db.ingredients.find(), categories=mongo.db.categories.find())
    

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    recipes = mongo.db.recipes
    this_recipe = recipes.insert_one(request.form.to_dict())
    recipe_id = this_recipe.inserted_id
    recipe_image = request.files['recipe_image']
    mongo.save_file(recipe_image.filename, recipe_image, base='fs', content_type = 'image', recipe_id = recipe_id )
    this_image = mongo.db.fs.files.find_one({"recipe_id": recipe_id})
    image_id = this_image.get('_id')
    image_name = this_image.get('filename')
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "$set":{
            'image_id' :image_id,
            'image_name' : image_name 
            }
     })
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_ingredients = mongo.db.ingredients.find()
    all_categories = mongo.db.categories.find()
    return render_template('edit_recipe.html', recipe=this_recipe, ingredients=all_ingredients, categories=all_categories)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    mongo.db.fs.files.remove({'recipe_id':ObjectId(recipe_id)})
    recipe_image = request.files['recipe_image']
    mongo.save_file(recipe_image.filename, recipe_image, base='fs', content_type = 'image', recipe_id = recipe_id )
    new_image = mongo.db.fs.files.find_one({"recipe_id": recipe_id})
    image_id = new_image.get('_id')
    image_name = new_image.get('filename')
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'description':request.form.get('description'),
        'category_name':request.form.get('category_name'),
        'ingredient_name': request.form.getlist('ingredient_name'),
        'method': request.form.get('method'),
        'image_id' : image_id,
        'image_name' : image_name
     })

    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    mongo.db.fs.files.remove({"recipe_id": ObjectId(recipe_id)})
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes')) 


@app.route('/get_ingredients')
def get_ingredients():
    return render_template("ingredients.html", ingredients=mongo.db.ingredients.find())

@app.route('/create_ingredient', methods=['POST'])
def create_ingredient():
    ingredients = mongo.db.ingredients
    ingredients.insert_one(request.form.to_dict())
    return render_template("ingredients.html", ingredients=mongo.db.ingredients.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
            