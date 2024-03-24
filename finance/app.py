import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def get_row_color(shares):
    if shares > 0:
        return "positive-row"
    else:
        return "negative-row"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT share_name, price, symbol, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY share_name",
        session["user_id"],
    )
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = cash[0]["cash"]
    total_stocks = 0
    for stock in stocks:
        total_stocks += stock["price"] * stock["SUM(shares)"]
        stock["price"] = usd(stock["price"])
    total = cash + total_stocks
    return render_template(
        "index.html",
        shares=stocks,
        cash=usd(cash),
        total=usd(total),
        total_stocks=usd(total_stocks),
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Must give symbol")

        result = lookup(symbol.upper())

        if not result:
            return apology("Symbol does not exist")

        if not shares:
            return apology("Get an amount of shares")
        try:
            shares = int(shares)
        except:
            return apology("Get an numeric integer of shares")

        if shares < 0:
            return apology("Buy more shares")

        share_price = lookup(symbol.upper())
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        total_price = share_price["price"] * shares

        if total_price > cash[0]["cash"]:
            return apology("Cannot afford")

        db.execute(
            "INSERT INTO transactions(user_id, share_name, price, symbol, shares) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            share_price["name"],
            share_price["price"],
            symbol.upper(),
            shares,
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            (cash[0]["cash"] - total_price),
            session["user_id"],
        )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"]
    )

    return render_template("history.html", shares=stocks, get_row_color=get_row_color)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must give symbol")

        result = lookup(symbol.upper())

        if not result:
            return apology("Symbol does not exist")

        result["price"] = usd(result["price"])

        return render_template("quoted.html", symbols=result)

    else:
        return render_template("quote.html")


@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def changepwd():
    """Change password"""
    if request.method == "POST":
        name = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not name:
            return apology("Put in your username")

        if not old_password:
            return apology("Put in your old password")

        if not new_password:
            return apology("Put in your new password")

        if not confirmation:
            return apology("Put in your confirmation")

        if new_password != confirmation:
            return apology("Password and confirmation is not the same")

        old_user = db.execute("SELECT * FROM users WHERE username = ?", name)

        # Ensure username exists and password is correct
        if len(old_user) != 1 or not check_password_hash(
            old_user[0]["hash"], old_password
        ):
            return apology("invalid username and/or password", 403)

        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new_password),
            old_user[0]["id"],
        )

        return redirect("/")
    else:
        return render_template("changepassword.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not name:
            return apology("Put in your username")

        if not password:
            return apology("Put in your password")

        if not confirmation:
            return apology("Put in your confirmation")

        if password != confirmation:
            return apology("Password and confirmation is not the same")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users(username, hash) VALUES (?, ?)", name, hash
            )
        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id,
        )
        return render_template(
            "sell.html", symbols=[row["symbol"] for row in symbols_user]
        )
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Must Give Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")

        if shares < 0:
            return apology("Share Not Allowed")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            user_id,
            symbol,
        )
        user_shares_real = user_shares[0]["shares"]

        if shares > user_shares_real:
            return apology("You Do Not Have This Amount Od Shares")

        uptd_cash = user_cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        db.execute(
            "INSERT INTO transactions (user_id, share_name, symbol, shares, price) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            stock["symbol"],
            (-1) * shares,
            stock["price"],
        )

        flash("Sold!")

        return redirect("/")
