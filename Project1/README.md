# Project 1

Web Programming with Python and JavaScript

File descriptions

application.py:  Of course, this is the main file.  A list of functions is as follows:
    - index() : main page, which is just the login page
    - check_new_username() : this checks if a suggested username is free
    - login_check() : this checks to see if the correct password is entered for an attempted login
    - logout_proc() : this ends the session when someone clicks the logout button
    - search_page() : this is the page to search for books from
    - get_results() : this collects the search results
    - back_to_results() : this goes back to the last set of search results
    - book_details(b_id) : this displays all the information for a given book as well as the reviews and a form for the
          user to leave a review if they haven't already done so
    - submit_review(book_id) : this is the procedure for the user's review to be recorded in the database
    - isbn_api(b_isbn) : this creates the API data for a given book, with ISBN as part of the url

Template files
book_page.html : Displays the book info, reviews, ratings
error.html : Error page
index.html : main/login page
layout.html : This is the general layout page, used in all other pages
search_results.html : Displays the results of a search
search.html : Contains the forms to initiate a book search
success.html : General page when an action is successful (e.g., account creation, logout)
test

Database info:
https://data.heroku.com/datastores/3dd940ab-83d5-4f09-9e28-2afb43abae31#administration
