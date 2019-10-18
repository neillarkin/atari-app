import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'recipe_db'
app.config['MONGO_URI'] = 'mongodb+srv://root:r00tUser@myfirstcluster-tbkzy.mongodb.net/recipe_db?retryWrites=true&w=majority'


mongo = PyMongo(app) #constructor method


# GAME PAGES ################

@app.route('/')
@app.route('/get_games')
def get_games():
    return render_template("games.html", games=mongo.db.games.find())


@app.route('/get_artist/<names>')
def get_artist(names):
    for name in names:
        print(names[name])
        
@app.route('/new_game')
def new_game():
    return render_template('new_game.html', years=mongo.db.years.find(), developers=mongo.db.developers.find())


# Create a Game in to the games docuemnt. Then create a screenshot in to the files document. 
# Next create a cover image in to the files documnet with the screenshots ID as attribute
# Then use the screenshot ID to find the cover image. Finally add the required attributs of the cover image in to the game document
  
@app.route('/create_game', methods=['POST'])
def create_game():
    games = mongo.db.games
    game_title = request.form.get('game_title') 
    game_year = request.form.get('game_year') 
    description= request.form.get('description')	
    developer_list = request.form.getlist('developer_name')
    this_game = games.insert_one({'game_title': game_title, 'game_year': game_year, 'developer_name' : developer_list, 'description': description, })
    game_id = this_game.inserted_id
    screenshot = request.files['screenshot']
    mongo.save_file(screenshot.filename, screenshot, base='fs', content_type = 'image', game_id = ObjectId(game_id) )
    this_screenshot_image = mongo.db.fs.files.find_one({"game_id": ObjectId(game_id)})
    this_screenshot_image_id = this_screenshot_image['_id']
    this_screenshot_image = this_screenshot_image['filename']
    cover_image = request.files['cover_image']
    mongo.save_file(cover_image.filename, cover_image, base='fs', content_type = 'image', game_id = ObjectId(game_id), screenshot_id = this_screenshot_image_id, screenshot_image = this_screenshot_image )
    this_image = mongo.db.fs.files.find_one({"screenshot_id": ObjectId(this_screenshot_image_id)})
    games.update( {'_id': ObjectId(game_id)},
    {
        "$set":{
            'cover_id' : this_image.get('_id'),
            'cover_image' : this_image.get('filename'),
            'screenshot_id' : this_image.get('screenshot_id'),
            'screenshot_image' : this_image.get('screenshot_image'),
            }
     }) 
    return redirect(url_for('get_games')) 

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    mongo.db.fs.files.remove({"game_id": ObjectId(game_id)})
    # return redirect(url_for('get_recipes')) 
    # return redirect(url_for('get_recipes'))  
    
@app.route('/modal_create_developer', methods=['POST'])
def modal_create_developer():
    developers = mongo.db.developers
    developers.insert_one(request.form.to_dict())
    return render_template("list_section.html", developers=mongo.db.developers.find())

@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    this_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_developers = mongo.db.developers.find()
    all_years = mongo.db.years.find()
    all_files =  mongo.db.fs.files.find()
    return render_template('edit_game.html', files=all_files, game=this_game, years=all_years, developers=all_developers)


@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    mongo.db.fs.files.remove({'game_id': ObjectId(game_id)})
    screenshot = request.files['screenshot']
    mongo.save_file(screenshot.filename, screenshot, base='fs', content_type = 'image', game_id = ObjectId(game_id) )
    new_screenshot_image = mongo.db.fs.files.find_one({"game_id": ObjectId(game_id)})
    cover_image = request.files['cover_image']
    mongo.save_file(cover_image.filename, cover_image, base='fs', content_type = 'image', game_id = ObjectId(game_id), screenshot_id = new_screenshot_image['_id'], screenshot_image = new_screenshot_image['filename'] )
    new_image = mongo.db.fs.files.find_one({"screenshot_id": ObjectId(new_screenshot_image['_id'])})
    games = mongo.db.games
    games.update( {'_id': ObjectId(game_id)},
    {
        'game_title':request.form.get('game_title'),
        'game_year':request.form.get('game_year'),
        'developer_name': request.form.getlist('developer_name'),
        'description': request.form.get('description'),
        'cover_id' : new_image.get('_id'),
        'cover_image' : new_image.get('filename'),
        'screenshot_id' : new_image.get('screenshot_id'),
        'screenshot_image' : new_image.get('screenshot_image')
     })
    return redirect(url_for('get_games'))


# DEVELOPERS PAGES ##################

@app.route('/get_developers')
def get_developers():
    return render_template("developers.html", developers=mongo.db.developers.find())

@app.route('/create_developer', methods=['POST'])
def create_developer():
    developers = mongo.db.developers
    developers.insert_one(request.form.to_dict())
    return redirect(url_for('get_developers')) 
    
@app.route('/edit_developer/<developer_id>')
def edit_developer(developer_id):
    this_developer= mongo.db.developers.find_one({"_id": ObjectId(developer_id)})
    all_developers = mongo.db.developers.find()
    return render_template('edit_developer.html', developer=this_developer, developers=all_developers)

@app.route('/delete_developer/<developer_id>')
def delete_developer(developer_id):
    mongo.db.developers.remove({"_id": ObjectId(developer_id)})
    return redirect(url_for('get_developers')) 

@app.route('/update_developer/<developer_id>', methods=["POST"])
def update_developer(developer_id):
    developers = mongo.db.developers
    developers.update( {'_id': ObjectId(developer_id)},
    {
        'developer_name':request.form.get('developer_name')
    })
    return redirect(url_for('get_developers')) 


# YEARS



# ###########################################################################################
# ###########################################################################################
# ###########################################################################################
# ###########################################################################################
# ###########################################################################################
# ###########################################################################################

# ###########################################################################################
# ###########################################################################################
# ###########################################################################################


#route decorator is a URL that redirects to a Python function

@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find(), files=mongo.db.fs.files.find())


@app.route('/new_recipe')
def new_recipe():
    return render_template('new_recipe.html', ingredients=mongo.db.ingredients.find(), categories=mongo.db.categories.find())
    

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    recipes = mongo.db.recipes
    recipe_name = request.form.get('recipe_name') 
    description= request.form.get('description')	
    category_name = request.form.get('category_name')	
    ingredient_list = request.form.getlist('ingredient_name')	
    method = request.form.get('method')	
    this_recipe = recipes.insert_one({'recipe_name': recipe_name, 'description': description, 'category_name': category_name, 'ingredient_name' : ingredient_list,	'method' : method})
    recipe_id = this_recipe.inserted_id
    recipe_image = request.files['recipe_image']
    mongo.save_file(recipe_image.filename, recipe_image, base='fs', content_type = 'image', recipe_id = ObjectId(recipe_id) )
    this_image = mongo.db.fs.files.find_one({"recipe_id": ObjectId(recipe_id)})
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "$set":{
            'image_id' :this_image.get('_id'),
            'image_name' : this_image.get('filename')
            }
     }) 
    return redirect(url_for('get_recipes')) 


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_ingredients = mongo.db.ingredients.find()
    all_categories = mongo.db.categories.find()
    return render_template('edit_recipe.html', recipe=this_recipe, ingredients=all_ingredients, categories=all_categories)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    mongo.db.fs.files.remove({"recipe_id": ObjectId(recipe_id)})
    # return redirect(url_for('get_recipes')) 
    # return redirect(url_for('get_recipes')) 


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    mongo.db.fs.files.remove({'recipe_id': ObjectId(recipe_id)})
    recipe_image = request.files['recipe_image']
    mongo.save_file(recipe_image.filename, recipe_image, base='fs', content_type = 'image', recipe_id = ObjectId(recipe_id) )
    new_image = mongo.db.fs.files.find_one({"recipe_id": ObjectId(recipe_id)})
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'description':request.form.get('description'),
        'category_name':request.form.get('category_name'),
        'ingredient_name': request.form.getlist('ingredient_name'),
        'method': request.form.get('method'),
        'image_id' : new_image.get('_id'),
        'image_name' : new_image.get('filename')
     })
    return redirect(url_for('get_recipes')) 
    # return render_template("recipes.html", recipes=mongo.db.recipes.find())
    # return redirect(url_for('get_recipes'))




@app.route('/get_ingredients')
def get_ingredients():
    return render_template("ingredients.html", ingredients=mongo.db.ingredients.find())
    
@app.route('/create_ingredient', methods=['POST'])
def create_ingredient():
    ingredients = mongo.db.ingredients
    print (ingredients)
    ingredients.insert_one(request.form.to_dict())
    return redirect(url_for('get_ingredients')) 

@app.route('/modal_create_ingredient', methods=['POST'])
def modal_create_ingredient():
    ingredients = mongo.db.ingredients
    ingredients.insert_one(request.form.to_dict())
    return render_template("section.html", ingredients=mongo.db.ingredients.find())

# @app.route('/call_modal')
# def call_modal():
#     return ('#myDeleteModal')

# @app.route('/get_this_recipe/<recipe_id>')
# def get_this_recipe(recipe_id):
#     this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
#     return this_recipe.recipe_id
    
#     # return render_template('recipes.html' + '#myDeleteModal', recipe=this_recipe)
    

#  return redirect(url_for('get_recipes') + '#myDeleteModal')
#   return render_template('recipes.html', recipe=this_recipe, submission_successful=submission_successful)
    # return render_template(url_for('get_recipes') + '#myDeleteModal', recipe=this_recipe)
    # redirect(url_for('index') + '#myModal')


@app.route('/delete_ingredient/<ingredient_id>')
def delete_ingredient(ingredient_id):
    mongo.db.ingredients.remove({"_id": ObjectId(ingredient_id)})
    return redirect(url_for('get_ingredients')) 

@app.route('/edit_ingredient/<ingredient_id>')
def edit_ingredient(ingredient_id):
    this_ingredient = mongo.db.ingredients.find_one({"_id": ObjectId(ingredient_id)})
    all_ingredients = mongo.db.ingredients.find()
    return render_template('edit_ingredient.html', ingredient=this_ingredient, ingredients=all_ingredients)

@app.route('/update_ingredient/<ingredient_id>', methods=["POST"])
def update_ingredient(ingredient_id):
    ingredients = mongo.db.ingredients
    ingredients.update( {'_id': ObjectId(ingredient_id)},
    {
        'ingredient_name':request.form.get('ingredient_name')
    })
    return redirect(url_for('get_ingredients')) 


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
            
