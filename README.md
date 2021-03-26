# Milestone Project 3 – Data Centric Development.
# Atari game app with Python and MongoDB 

## Overview
The app is a demonstrates Python capabilities with the Flask framework and Jinga templates by performing CRUD operations on collections of documents stored in the NoSQL environment MongoDB. 

A live version of the app is hosted here:
 https://atari-app-neil.herokuapp.com 

Project code is is available here: https://github.com/neillarkin/atari-app 

## WireFrame
#### Mobile
https://github.com/neillarkin/atari-app/blob/master/wireframe/mobile-views.JPG

#### Desktop
https://github.com/neillarkin/atari-app/blob/master/wireframe/desktop-views.JPG

#### Relational Database
https://github.com/neillarkin/atari-app/blob/master/wireframe/realtion-model.JPG

## UX
The primary target user of the application is a potential employer. The application will be used to showcase some of my knowledge of using templates with Python to store and retrieve data on a NoSQL database. It is expected that the employer will only spend a few moments using the application and so it should appear simple and visually appealing. The UI is clean and responsive with no major functional bugs that would give a poor user experience. The secondary target user is a gamer who it curious in old video games and wants to learn more about how they were made; specifically the art and artists involved with developing the games. The app attempts to show the stark contrast between the games box art and the actual 8-bit graphics of the game.

### Use case scenarios
The target use for this application is potential employers. A working version of the application will be displayed on my portfolio website along with the source code. The application will be used as part of an interview pitch to convey my knowledge of working with an API and other related technologies.
A second scenario could be curious video gamers who are interested in the playing old Atari games from the 1970’s and 1980’s. Each game card displays a play button that directs the user to a location where they can purchase an Atari 2600 emulator hosted on Steam.

## Features
The application has a number of features. A user can view a list of game art, create a new game card and edit or delete a card. A user can also view a list of artists, create a new artist  and edit or delete an artist. A button also directs the user to an Atari 2600 emulator.
A user can also add an artist from the Edit page and that list will update immediately without leaving the Edit page.
The app uses a one-to-many relationship between games and artists. One game can have many artists. Each artists’ Object ID is intended to be used as a foreign key in each game document.
This relationship enables a game card to display a list of artists that worked on that game. Extended functionality allows each artist to display the games that they have worked on. 

## Features to implement
The application stores an array or artist names in each game card. This will lead to a bug if two artist names are the same. The code should be adjusted to store each artist ID then use that unique ID to find the artists name.
An other future feature will be to create a template for each artist profile then hyperlink to that template from the game card. 
The home pure age displays a row of cards that have different image sizes. A Jinga loop was used to display the cards in a more random but aligned fashion. A future feature would be to create a function that would find the image size then adjust the div sizes to fit comfortably in to place. The function could have a maximum and minimum boundaries and output CSS class names depending on the image size. The image dimensions may need to be stored in the documents fields.
Some of the JavaScript functions are reusable, e.g. displayToast(). A future plan would be to make more of the functions suchs as calling the modal, reusable.
Card size depends on original image dimensions. The small card sizes have layout issues that must be addressed such as text wrapping.

## Relational database
The app uses MongoDB to store three collections called games, developers and years. GridFS is used to create two more collections (fs.files & fs.chunks) are used to store image files.
The app uses a one-to-many relationship between games and artists(developers). One game can have many artists. Each artists’ Object ID is intended to be used as a foreign key in each game document.

## Technologies
Python 3 is used for core functions with Flask 1.1.1 for routing. Jinga 2.10.1 is used for templating with Pymongo 3.8. The NoSql database is MongoDB version 4.0.13.
The Materialize 1.0 framework is used for grid layout, forms and lists. 
JavaScript and JQuery 4.4.1 are  used for some div manipulations. Parallax 1.5.0 is used for background scrolling.
A complete list of technologies is in the Requirements.txt file


## Testing
Test-driven development was implemented with Pythons’ ‘assert’ function and the byotest.py script. Four tests were complete: test_are_equal(), test_are_not_equal(), test_is_in() and test_is_not_in()
(Lines 172 of run.py) 
The first test calls the test_are_equal() function and checks if an actual value is equal to an expected value. It takes two parameters, actual and expected. The first being a function called get_developers_test() which returns the actual value and the second is the expected value. The get_developers_test() function searches the ‘developers’ collection for the actual parameter and returns it. The test_are_equal() then compares the result with the expected parameter. The test_are_not_equal()  function uses the same parameters except an incorrect value is intentionally given for the actual parameter. 
The test_is_in() function takes checks if a value is in a collection. It takes two parameters collection and item. The first parameter is the return of a function called get_developers_collection_test() which returns an array of the values in the developers collection. The second parameter is called item. The get_developers_collection_test() checks if the item value is present in the returned collection array. 
The final test uses the test_not_in() function with the get_developers_collection_test()  as a parameter and an intentionally incorrect value for item.

Manual testing was performed with Chrome on Windows, Chrome on Android, and Safari on iOS. The test cases were as below:
    1. Click a game card. Edit its contents then Save it. Verify you changes were implemented on the front-end and in the collection. 
    2. Click a game card and delete it. Verify you changes were implemented on the front-end and in the collection. 
    3.  Click an artist name and edit it then save it. Verify you changes were implemented on the front-end and in the collection. 
    4. Click an artist name and delete it. Verify you changes were implemented on the front-end and in the collection. 
    5. Click a game card and delete it. Verify the card has been removed from the collection.
    6. Perform steps 1 to 5 with Safari on iOS
    7. Perform steps 1 to 5 with Chrome on Android

### Bugs/Issues
Duplicate artist names may cause errors because a game document stores the actual artist string name rather than the artists unique Object ID as a foreign-key in a typical one-to-many relationship. The artist name could then be retrieved by using its ID  and a nested loop.

### Deployment
The sites was built on the AWS Cloud 9 IDE with GitHub used to backup milestones in development. 
The latest version is hosted on Heroku and is available here: https://atari-app-neil.herokuapp.com/ 
Project source code is available on GitHub: https://github.com/neillarkin/atari-app 

#### Credits and Sources
- The concept was taken from the book Art of Atari by Tim Lapetino (Dynamite Entertainment (October 25, 2016),  ISBN-13: 978-1524101039)
- Animated logo code was sourced from: https://codepen.io/lbebber/pen/ypgql
- The Atari SF font was created from www.onlinewebfonts.com and licensed by CC 3.0
- The Atari logo SVG was sourced here and then converted to a font. https://www.flaticon.com/free-icon/atari_813422
