# Project 3a

Web Programming with Python and JavaScript

###2019.01.20
17:42 Ran migration, it seems you can't create superuser without doing this
first

17:42 Created superuser
name: michael
email: gmail
password: rm4582slp

###2020.01.29
20:25 Plan to implement Shopping Cart
- create class Order for the shopping cart/order
- create class OrderItem which will essentially be a menu item and a quantity
- an (instance of the class) Order will have some further properties, like
whether it is active, whether it has been submitted or cancelled
- there will be at most one active Order and to look at the shopping cart we
will display the associated items

###2020.01.30
11:22
- when you sign in, need to check if there is an active order; if not, we
should open one

13:00
There are a lot of things to do
- Page to view order
- Buttons to view order
- Buttons to cancel order

###2020.01.31
13:37 Most of the features required for the project work at a basic level now.
Here is a list of things that could be improved:
- there is a small problem now after a user submits an order, whether a new
one should be initiated right away
- option to edit or delete order items
- option to cancel a whole order
- staff can view items in an order (not possible now)
- database queries for staff to see use of ingredients

14:34
The issue about the non-existent orders seems to be cleared up.
