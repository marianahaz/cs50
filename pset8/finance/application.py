import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# API KEY: pk_a16b04efc4ec4cc9982997a242be415c

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():

    # Store current user session id
    currentId = session["user_id"]

    # Get all stocks
    portfolio = db.execute("SELECT * FROM stocks WHERE user = :user", user=currentId)

    # Empty list for the stocks symbols
    allStocks = []
    lines = ""
    grandTotal = 0

    if len(portfolio) == 0:
        lines = "<h3 style='margin-bottom:20px;'>You currently have 0 stocks</h3>"
    else:
        for i in range(len(portfolio)):
            currentStock = portfolio[i]['symbol']

            allStocks.append(currentStock)

            stockInfo = lookup(currentStock)

            name = stockInfo["name"]
            price = stockInfo["price"]
            shares = db.execute("SELECT shares FROM stocks WHERE user = :user AND symbol = :symbol", user = currentId, symbol = currentStock)[0]["shares"]
            totalStock = price * shares

            grandTotal = grandTotal + totalStock

            lines = lines + "<tr><td><b>" + currentStock.upper() + "</b></td><td>" + name + "</td><td>" + str(shares) + "</td><td>" + str(usd(price)) + "</td><td>" + str(usd(totalStock)) + "</td></tr>"

    cashAvailable = db.execute("SELECT cash FROM users WHERE id = :user", user=currentId)[0]['cash']

    grandTotal = grandTotal + cashAvailable

    return render_template("index.html", lines=lines, cashAvailable = usd(cashAvailable), grandTotal = usd(grandTotal))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == 'GET':
        return render_template("buy.html")

    else:
        stock = request.form.get("stock")
        shares = int(request.form.get("shares"))

        if not stock or not shares:
             return apology("Please fill all fields", 403)

        if shares < 0:
             return apology("Please provide a valid input", 403)

        # Get stock information and lookup the price to get the purchase amount
        stockInfo = lookup(stock)
        totalPrice = stockInfo["price"] * float(shares)

        # Store current user session id
        currentId = session["user_id"]

        # Get how much cash the user has available
        userCash = db.execute("SELECT cash FROM users WHERE id = :user", user=currentId)[0]['cash']

        userCashAfter = userCash - totalPrice;

        # Return error if there isn't enough cash
        if userCashAfter < 0:
            return apology("You don't have enough for that", 403)
        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=userCashAfter, id = currentId)

        db.execute("CREATE TABLE IF NOT EXISTS 'stocks' ('purchase' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'user' INTEGER NOT NULL, 'symbol' TEXT NOT NULL, 'shares' NUMERIC NOT NULL);")

        # Create table to keep track of transactions
        db.execute("CREATE TABLE IF NOT EXISTS 'transactions' ('number' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user' INTEGER NOT NULL, 'type' TEXT NOT NULL, 'symbol' TEXT NOT NULL, 'price' NUMERIC NOT NULL, 'shares' NUMERIC NOT NULL, 'time' INTEGER NOT NULL)")

        # Check if the user already has any shares of that stock. If he does, update the number.
        hasStock = db.execute("SELECT symbol FROM stocks WHERE user = :id", id=currentId)

        userStocksList = list(({k: [d.get(k) for d in hasStock]
                                for k in set().union(*hasStock)
                                }).values())

        userStocks = []
        for myList in userStocksList:
            for item in myList:
                userStocks.append(item)



        # INSERT INTO TRANSACTIONS TABLE
        db.execute("INSERT INTO transactions (user, type, symbol, price, shares, time) VALUES (?, ?, ?, ?, ?, datetime('now'))", (currentId, 'buy', stock, stockInfo["price"], shares))



        if stock in userStocks:
            beforeShares = db.execute("SELECT shares FROM stocks WHERE user = :id AND symbol = :symbol", id=currentId, symbol=stock)[0]['shares']
            afterShares = beforeShares + shares
            db.execute("UPDATE stocks SET shares = :shares WHERE user = :id AND symbol = :symbol", shares=afterShares, id = currentId, symbol = stock)
            return redirect("/")

        # If the user doesn't have any shares of that stock, add stock symbol and shares to their id.
        else:
            db.execute("INSERT INTO stocks (user, symbol, shares) VALUES (?, ?, ?)", (currentId, stock, shares))
            return redirect("/")




        #else:

        #return render_template("validate.html", currentId = userCashAfter)


    #return apology("TODO")


@app.route("/history")
@login_required
def history():

    # Store current user session id
    currentId = session["user_id"]

    transactions = db.execute("SELECT * FROM transactions WHERE user = :user", user = currentId)

    lines = ''

    if len(transactions) == 0:
        lines = "<h3 style='margin-bottom:20px;'>You currently have no history of transactions</h3>"

    else:
        for i in range(len(transactions)):

            stock = transactions[i]['symbol']

            stockInfo = lookup(stock)

            price = stockInfo["price"]

            shares = transactions[i]['shares']

            if transactions[i]['type'] == "sell":

                shares = 0 - shares

            time = transactions[i]['time']


            lines = lines + "<tr><td><b>" + stock.upper() + "</b></td><td>" + str(shares) + "</td><td>" + str(usd(price)) + "</td><td>" + time + "</td></tr>"


    return render_template("history.html", lines = lines)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "GET":
        return render_template("quote.html")

    else:
        stockName = request.form.get("stock")

        # Typed an invalid symbol
        if not stockName:
            return apology("Please type a valid symbol", 403)

        # Use the lookup function to find the price of a stock
        stock = lookup(stockName)


        return render_template("quoted.html", name = stock["name"], symbol = stock["symbol"], price = stock["price"])


@app.route("/register", methods=["GET", "POST"])
def register():

    # User clicked on "register"
    if request.method == "GET":
        return render_template("register.html")

    else:
        user = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Error conditions

        if len(user) < 4:
            return apology("Username must be at least 4 characters", 403)
        if password != confirmation:
            return apology("Password doesn't match confirmation", 403)
        if not user or not password or not confirmation:
            return apology("You must provide all fields", 403)

        #all_usernames = db.execute("SELECT * FROM users WHERE username = user")
        #if user in all_usernames:
        #    return apology("This username is already in use", 403)

        hash = generate_password_hash(password)

        # Add user into database
        rows = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (user, hash))

        # Create session for recently registered user
        session["user_id"] = rows

        # Redirect user to index page
        return redirect("/")


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():

    if request.method == 'GET':
        return render_template("cash.html")

    else:

        currentId = session["user_id"]
        amount = float(request.form.get("amount"))


        cashBefore = db.execute("SELECT cash FROM users WHERE id = :user", user = currentId)[0]['cash']

        cashAfter = cashBefore + amount

        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = cashAfter, id = currentId)

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == 'GET':
        return render_template("sell.html")

    else:

        # Store current user session id
        currentId = session["user_id"]

        stock = request.form.get("stock")
        shares = int(request.form.get("shares"))

        if not stock or not shares:
             return apology("Please fill all fields", 403)

        if shares < 0:
             return apology("Please provide a valid input", 403)

        # Get the current amount of shares
        sharesBefore = db.execute("SELECT shares FROM stocks WHERE user = :user AND symbol = :symbol", user = currentId, symbol = stock)[0]['shares']

        # Get stock info
        stockInfo = lookup(stock)

        # Get user cash
        cashBefore = db.execute("SELECT cash FROM users WHERE id = :user", user = currentId)[0]['cash']

        # Compare to check the condition in which the transaction falls
        if shares > sharesBefore:
            return apology ("You can't sell more shares than you have", 403)




        # Update cash and check the condition to update or delete from the stocks table
        else:
            # Create table to keep track of transactions
            db.execute("CREATE TABLE IF NOT EXISTS 'transactions' ('number' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user' INTEGER NOT NULL, 'type' TEXT NOT NULL, 'symbol' TEXT NOT NULL, 'price' NUMERIC NOT NULL, 'shares' NUMERIC NOT NULL, 'time' INTEGER NOT NULL)")

            cashToGet = stockInfo["price"] * shares
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = cashBefore+cashToGet, id = currentId)


            # INSERT INTO TRANSACTIONS TABLE
            db.execute("INSERT INTO transactions (user, type, symbol, price, shares, time) VALUES (?, ?, ?, ?, ?, datetime('now'))", (currentId, 'sell', stock, stockInfo["price"], shares))



            if shares == sharesBefore:
                db.execute("DELETE FROM stocks WHERE user = :user AND symbol = :symbol", user = currentId, symbol = stock)
                return redirect("/")
            else:
                db.execute("UPDATE stocks SET shares = :shares WHERE user = :user AND symbol = :stock", shares = sharesBefore-shares, user = currentId, stock = stock)
                return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
