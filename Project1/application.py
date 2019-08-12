from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session

import datetime, requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://wgoeytjfrbnypa:e41b67b7351067f3d6f059fd6e16879e8a1d643e8a78da68b9a4399e7cfdf20e@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/d5fsnhhq7lj4g4")
db = scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["post", "get"])
def index():
    book_search = None
    if "current_username" in session:
        return render_template("index.html", current_user = session["current_username"])
    else:
        return render_template("index.html")

@app.route("/cnu", methods=["post"])
def check_new_username():
    """We want to check if the username is in the table 'users'.  If it is
    already there, then we want to issue an error.  Otherwise, we create a new
    account and forward to the search page """
    reg_username = request.form.get("reg_username")
    username_free = db.execute("SELECT username, password FROM users_test WHERE username = :id",
                        {"id": reg_username}).fetchone()

    if username_free == None: # Here we want to create a new account
        reg_password = request.form.get("reg_password")
        db.execute("INSERT INTO users_test (username, password) VALUES (:id, :pw)", {"id": reg_username, "pw": reg_password})
        db.commit()
        session["current_username"] = reg_username
        userid = db.execute("SELECT id FROM users_test where username = :id", {"id": reg_username}).fetchone()
        session["current_userid"] = userid[0]
        return render_template("success.html", message = "You have created a new account!", current_user = session["current_username"], current_userid = session["current_userid"])
    else: # Here we want to go to error page telling saying that the username exists
        return render_template("error.html", message="That username is already taken.  Try again with a new username.")

@app.route("/check_login", methods=["post"])
def login_check():
    login_username = request.form.get("login_username")
    login_password = request.form.get("login_password")
    db_userinfo = db.execute("SELECT password, id FROM users_test where username = :id", {"id" : login_username}).fetchone()
    if db_userinfo.password == login_password:
        session["current_username"] = login_username
        session["current_userid"] = db_userinfo.id
        return render_template("success.html", message="You have successfuly logged in!", current_user = session["current_username"])
    else:
        return render_template("error.html", message="The password does not match the username.")

@app.route("/logout", methods=["post"])
def logout_proc():
    session.pop("current_username")
    session.pop("current_userid")
    return redirect(url_for('index'))
    #render_template("success.html", message="You have successfuly logged out!")#, current_user = session["current_username"])

@app.route("/search", methods=["post", "get"])
def search_page():
    return render_template("search.html", current_user = session["current_username"])

@app.route("/results", methods=["post"])
def get_results():
    """Here we take the data from the search form and return a page with the search results"""
    au = request.form.get("author")
    ti = request.form.get("title")
    bn = request.form.get("isbn")
    y = request.form.get("year")
    search_terms = "where "
    if not(au==""):
        search_terms += "author like concat('%', concat(:auth,'%'))"
    if not(ti==""):
        if len(search_terms) < 7:
            search_terms += "title like concat('%', concat(:title,'%'))"
        else:
            search_terms += "and title like concat('%', concat(:title,'%'))"
    if not(bn==""):
        if len(search_terms) < 7:
            search_terms += "isbn like concat('%', concat(:bn,'%'))"
        else:
            search_terms += "and isbn like concat('%', concat(:bn,'%'))"
    if not(y==""):
        if len(search_terms) < 7:
            search_terms += "year = :year"
        else:
            search_terms += "and year = :year"
    search_terms += " order by year desc;"

    session["last_search"] = db.execute("SELECT * FROM books " + search_terms, {"auth": au, "title": ti, "bn": bn, "year": y}).fetchall()

    return render_template("search_results.html", books=session["last_search"], current_user = session["current_username"])

@app.route("/results_back", methods=["get", "post"])
def back_to_results():
    return render_template("search_results.html", books=session["last_search"], current_user = session["current_username"])

@app.route("/books/<int:b_id>")
def book_details(b_id):
    """Lists book details and reviews for a given book"""

    # Get the book details
    details = db.execute("SELECT title, author, isbn, year, id FROM books WHERE id = :book_id",
                            {"book_id": b_id}).fetchone()
    reviews = db.execute("SELECT reviews.review as review, reviews.rating as rating, reviews.review_date as rev_date, users_test.username as reviewer FROM reviews left join users_test on users_test.id = reviews.user_id WHERE book_id = :bk_id order by reviews.review_date desc", {"bk_id": b_id}).fetchall()
    reviewers = [ review.reviewer for review in reviews ]
    al_revd = session["current_username"] in reviewers
    pms = { "key" : "TNDHWVNiRFkRMBueHIM3Bw" }
    pms["isbns"] = str(details.isbn)
    goodreads_info = requests.get("https://www.goodreads.com/book/review_counts.json", params = pms).json()['books'][0]

    return render_template("book_page.html", book_details=details, book_reviews=reviews, current_user = session["current_username"], already_reviewed = al_revd, gr_avg=goodreads_info["average_rating"], gr_revs=goodreads_info["work_ratings_count"])

@app.route("/review_submission/<int:book_id>", methods = ["post"])
def submit_review(book_id):
    """This is the procedure for a review to be written to the permanent database"""
    rev = request.form.get("review_text")
    rat = int(request.form.get("rating"))
    db.execute("INSERT INTO reviews (user_id, review, book_id, rating) VALUES (:id, :rev_txt, :b_id, :r )", {"id": session["current_userid"], "rev_txt": rev, "b_id": book_id, "r": rat})
    db.commit()
    return render_template("success.html", message = "Your review has been submitted.")

@app.route("/api/<b_isbn>", methods = ["get"])
def isbn_api(b_isbn):
    """Return details about book in our database"""

    # Make sure book is in database
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn_here", {"isbn_here" : b_isbn}).fetchone()
    if book is None:
        return jsonify({ "Error": "ISBN is not in database"}), 404
    revs = db.execute("SELECT count(review) FROM reviews WHERE book_id = :b_id", {"b_id" : book.id}).fetchone()
    avg_rating = db.execute("SELECT avg(rating) FROM reviews WHERE book_id = :b_id", {"b_id" : book.id}).fetchone()
    book_dict = {"title": book.title, "author": book.author, "year": book.year, "isbn": b_isbn, "review_count": revs[0], "average_score": float(avg_rating[0])}

    return jsonify(book_dict)
