import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from byotest import *

app = Flask(__name__)
usr = 'root'
pw = 'r00tUser'

app.config["MONGO_DBNAME"] = 'recipe_db'
app.config['MONGO_URI'] = 'mongodb+srv://' + usr + ':' + pw + '@myfirstcluster-tbkzy.mongodb.net/recipe_db?retryWrites=true&w=majority'

# Constructor method
mongo = PyMongo(app) 


################################
# GAME VIEWS  ##################
################################

@app.route('/')
@app.route('/get_games')
def get_games():
    return render_template("games.html", games=mongo.db.games.find())


@app.route('/new_game')
def new_game():
    return render_template('new_game.html', years=mongo.db.years.find(), developers=mongo.db.developers.find())


# 1) Create a Game in to the games document. Then create a screenshot in to the files document. 
# 2) Next create a cover image in to the files documnet with the screenshots ID as an attribute
# 3) Then use the screenshot ID to find the cover image. 
# 4) Finally add the required attibutes of the cover image in to the game document
@app.route('/create_game', methods=['POST'])
def create_game():
    games = mongo.db.games
    developers = mongo.db.developers
    game_title = request.form.get('game_title') 
    game_year = request.form.get('game_year') 
    description= request.form.get('description')	
    developer_list = request.form.getlist('developer_name')
    this_game = games.insert_one({'game_title': game_title, 'game_year': game_year, 'developer_name' : developer_list, 'description': description, })
    game_id = this_game.inserted_id
    
    cover_image = request.files['cover_image']
    mongo.save_file(cover_image.filename, cover_image, base='fs', content_type = 'image', game_id_cover = ObjectId(game_id))
    this_cover = mongo.db.fs.files.find_one({"game_id_cover": ObjectId(game_id)})
    
    screenshot = request.files['screenshot']
    mongo.save_file(screenshot.filename, screenshot, base='fs', content_type = 'image', game_id_screenshot = ObjectId(game_id))
    this_screenshot = mongo.db.fs.files.find_one({"game_id_screenshot": ObjectId(game_id)})  
    
    games.update( {'_id': ObjectId(game_id)},
    {
        "$set":{
            'cover_image' : this_cover.get('filename'),
            'screenshot_image' : this_screenshot.get('filename'),
            }
     }) 
    return redirect(url_for('get_games')) 

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    mongo.db.fs.files.remove({"game_id_cover": ObjectId(game_id)})
    mongo.db.fs.files.remove({"game_id_screenshot": ObjectId(game_id)})

    
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
    screenshot = request.files['screenshot']
    cover_image = request.files['cover_image']
    current_cover = mongo.db.fs.files.find_one({"game_id_cover": ObjectId(game_id)})
    current_screenshot = mongo.db.fs.files.find_one({"game_id_screenshot": ObjectId(game_id)})
    games = mongo.db.games
    updated_game = {
        'game_title':request.form.get('game_title'),
        'game_year':request.form.get('game_year'),
        'developer_name': request.form.getlist('developer_name'),
        'description': request.form.get('description'),
        'cover_image': current_cover.get('filename'),
        'screenshot_image': current_screenshot.get('filename'),
     }
    if cover_image:
        mongo.db.fs.files.remove({'game_id_cover': ObjectId(game_id)})
        mongo.save_file(cover_image.filename, cover_image, base='fs', content_type = 'image', game_id_cover = ObjectId(game_id))
        new_cover = mongo.db.fs.files.find_one({"game_id_cover": ObjectId(game_id)})
        updated_game['cover_image'] = new_cover.get('filename')

    if screenshot:
        mongo.db.fs.files.remove({'game_id_screenshot': ObjectId(game_id)})
        mongo.save_file(screenshot.filename, screenshot, base='fs', content_type = 'image', game_id_screenshot = ObjectId(game_id))
        new_screenshot = mongo.db.fs.files.find_one({"game_id_screenshot": ObjectId(game_id)})
        updated_game['screenshot_image'] = new_screenshot.get('filename')

    games.update( {'_id': ObjectId(game_id)},updated_game)
    return redirect(url_for('get_games'))


#################################
# ARTIST/DEVELOPER VIEWS ##################
#################################

#Note: 'artists' are referred to as 'developers'

@app.route('/get_developers')
def get_developers():
    developers=mongo.db.developers.find()
    developers_list = list(developers)
    games_developers = mongo.db.games.find({},{"game_title", "developer_name", "cover_image"})
    games_developers_list = list(games_developers)
    badge_list = []
    for dev in developers_list:
        count = 0;
        badge = dict(developer_name = dev['developer_name'], game_count = count)
        for game in games_developers_list:
            if dev['developer_name'] in game['developer_name']:
                count = count + 1
                badge["game_count"] = count
        badge_list.append(badge) 
    return render_template("developers.html", games_developers_list=games_developers_list, developers_list=developers_list, badge_list=badge_list)

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


#################################
# TESTS ################## 
#################################

def get_developers_test(name):
    developers = mongo.db.developers.find()
    for x in developers:
        if name in x['developer_name']:
            return x['developer_name']

test_are_equal(get_developers_test('George Opperman'),'George Opperman' )
test_not_equal(get_developers_test('Fake Name'),'George Opperman' )


def get_developers_collection_test():
    developers = mongo.db.developers.find()
    collection = []
    for x in developers:
        collection.append(x['developer_name'])
    return collection

test_is_in(get_developers_collection_test(),'George Opperman')
test_not_in(get_developers_collection_test(),'Fake Name')

# END TESTING #####################


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
            
