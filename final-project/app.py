from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure the database
db = sqlite3.connect('info.db', check_same_thread=False)
cursor = db.cursor()

# CREATE ALL TABLES
db.execute("CREATE TABLE IF NOT EXISTS 'lists' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'list_name' TEXT NOT NULL);")
db.execute("CREATE TABLE IF NOT EXISTS 'entries' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'list_name' TEXT NOT NULL, 'character' TEXT NOT NULL, 'pinyin' TEXT NOT NULL, 'translation' TEXT NOT NULL, 'link' TEXT NOT NULL);")

@app.route("/")
def home():

    cursor.execute("SELECT list_name FROM lists")
    allLists = cursor.fetchall()
    printLists = ''
    if len(allLists) == 0:
        printLists = "<option value=''>--No lists--</option>"
    else:
        for item in allLists:
            myList =  ''.join(item)
            myListId = myList.replace(" ", "")
            printLists = printLists + '<option value="' + myListId + '">' + myList + '</option>'

    
    cursor.execute("SELECT id FROM entries ORDER BY id DESC LIMIT 5")
    lastAddedId = cursor.fetchall()

    printLastAdded = ''
        
    if len(lastAddedId) == 0:
        printLastAdded = "<p class='empty-last-added'>You haven't added any entries in your lists.</p>"
        
    for item in lastAddedId:
        #identify everything based on the id

        item = int(item[0])

        cursor.execute("SELECT character FROM entries WHERE id = :item", {"item": item})
        character = cursor.fetchone()
        character = ''.join(character)

        cursor.execute("SELECT pinyin FROM entries WHERE id = :item", {"item": item})
        pinyin = cursor.fetchone()
        pinyin = ''.join(pinyin)
        
        cursor.execute("SELECT translation FROM entries WHERE id = :item", {"item": item})
        translation = cursor.fetchone()
        translation = ''.join(translation)
        
        cursor.execute("SELECT link FROM entries WHERE id = :item", {"item": item})
        link = cursor.fetchone()
        link = ''.join(link)

        printLastAdded = printLastAdded + '<li><div class="entry-image"><img src="'+ link +'"></div><div class="entry-info"><span class="character">'+ character +'</span><br><span class="pinyin">' + pinyin + '</span><br><span class="translation">'+ translation + '</span></div></li>'

    
    return render_template("/index.html", printLists = printLists, printLastAdded = printLastAdded)



@app.route("/mylists", methods=["GET", "POST"])
def mylists():

    cursor.execute("SELECT list_name FROM lists")
    allLists = cursor.fetchall()
    printLists = ''
    if len(allLists) == 0:
        printLists = "<p class='empty-list'>You don't have any lists.</p>"
    
    else:



        for item in allLists:
            myList =  ''.join(item)
            myListId = myList.replace(" ", "")
            printLists = printLists + '<div class="list-box"><div class="list-box-header"><button class="list-button collapsed" data-toggle="collapse" data-target="#' + myListId + '">'+myList+'<span></span></button></div><div id="'+ myListId +'" class="collapse" data-parent="#accordion"><div class="list-box-body"><ul>'
            
            cursor.execute("SELECT character FROM entries WHERE list_name = :list_name", {"list_name": myListId})
            allCharacters = cursor.fetchall()

            if len(allCharacters) == 0:
                printLists = printLists + '<p class="empty-list">There are no entries in this list</p>'

            for character in allCharacters:
                character = ''.join(character)

                cursor.execute("SELECT pinyin FROM entries WHERE list_name = :list_name AND character = :character", {"list_name": myListId, "character": character})
                pinyin = cursor.fetchone()
                pinyin = ''.join(pinyin)
                
                cursor.execute("SELECT translation FROM entries WHERE list_name = :list_name AND character = :character", {"list_name": myListId, "character": character})
                translation = cursor.fetchone()
                translation = ''.join(translation)
                
                cursor.execute("SELECT link FROM entries WHERE list_name = :list_name AND character = :character", {"list_name": myListId, "character": character})
                link = cursor.fetchone()
                link = ''.join(link)

                printLists = printLists + '<li><div class="entry-image"><img src="' + link + '"></div><div class="entry-info"><span class="character">' + character + '</span><br><span class="pinyin">' + pinyin + '</span><br><span class="translation">' + translation + '</span></div></li>'
            
            
            printLists = printLists + '</ul></div></div></div>'

    if request.method == 'POST':

        listName = request.form.get("add-list")

        db.execute("INSERT INTO lists (list_name) VALUES (?)", (listName,))
        db.commit()

        return redirect("/mylists")
    

    else: 
        return render_template("/mylists.html", listName = printLists)




@app.route("/find", methods=["GET", "POST"])
def find():

    if request.method == "GET":
        return render_template("/find.html")

    else:
        searchWord = request.form.get("searchWord")
        printResults = ''

        cursor.execute("SELECT id FROM entries WHERE character LIKE ?", ('%'+searchWord+'%', ))
        wordId = cursor.fetchall()
        
        searchResultsLength = len(wordId)

        if searchResultsLength == 0:
            printResults = "<p class='empty-search-results'>You don't have anything with this/these character(s) in your lists.</p>"
        
        for item in wordId:

            item = int(item[0])

            cursor.execute("SELECT character FROM entries WHERE id = :item", {"item": item})
            character = cursor.fetchone()
            character = ''.join(character)

            cursor.execute("SELECT pinyin FROM entries WHERE id = :item", {"item": item})
            pinyin = cursor.fetchone()
            pinyin = ''.join(pinyin)
            
            cursor.execute("SELECT translation FROM entries WHERE id = :item", {"item": item})
            translation = cursor.fetchone()
            translation = ''.join(translation)
            
            cursor.execute("SELECT link FROM entries WHERE id = :item", {"item": item})
            link = cursor.fetchone()
            link = ''.join(link)
            
            printResults = printResults + '<li><div class="entry-image"><img src="' + link + '"></div><div class="entry-info"><span class="character">' + character + '</span><br><span class="pinyin">' + pinyin + '</span><br><span class="translation">' + translation + '</span></div></li>'

        searchResults = '<p>Results for ' + searchWord + ' (' + str(searchResultsLength) + ')</p>'
        
        return render_template("/find.html", printResults = printResults, searchResults = searchResults)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "GET":
        cursor.execute("SELECT list_name FROM lists")
        allLists = cursor.fetchall()
        printLists = ''
        if len(allLists) == 0:
            printLists = "<option value=''>--No lists--</option>"
        else:
            for item in allLists:
                myList =  ''.join(item)
                myListId = myList.replace(" ", "")
                printLists = printLists + '<option value="' + myListId + '">' + myList + '</option>'
        return render_template("/add.html", printLists = printLists)

    else:

        cursor.execute("SELECT list_name FROM lists")
        allLists = cursor.fetchall()
        printLists = ''
        if len(allLists) == 0:
            printLists = "<option value=''>--No lists--</option>"
        else:
            for item in allLists:
                myList =  ''.join(item)
                myListId = myList.replace(" ", "")
                printLists = printLists + '<option value="' + myListId + '">' + myList + '</option>'

        listToAdd = request.form.get('add-list')
        listToAdd = ''.join(listToAdd)
        listToAdd = listToAdd.replace(" ", "")
        character = request.form.get('add-character')
        pinyin = request.form.get('add-pinyin')
        translation = request.form.get('add-translation')
        link = request.form.get('add-image')

        db.execute("INSERT INTO entries (list_name, character, pinyin, translation, link) VALUES (?, ?, ?, ?, ?)", (listToAdd, character, pinyin, translation, link))
        db.commit()

        message = "<p class='success-message'><b>"+ character + "</b> has been successfully added!</p>"

        return render_template("/add.html", message = message, printLists = printLists)


@app.route("/about")
def about():
    return render_template("about.html")
