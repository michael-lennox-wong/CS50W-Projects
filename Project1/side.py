# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:41:19 2019

@author: micha
"""

from flask import Flask, render_template, request

import datetime
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#%%
engine = create_engine("postgres://wgoeytjfrbnypa:e41b67b7351067f3d6f059fd6e16879e8a1d643e8a78da68b9a4399e7cfdf20e@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/d5fsnhhq7lj4g4")
db = scoped_session(sessionmaker(bind=engine))
#%%
x = db.execute("SELECT password FROM users_test where username = :id", {"id" : 'oma'}).fetchone()
#%%
au = "Will" #request.form.get("author")
ti = '' #request.form.get("title")
bn = '' #request.form.get("isbn")
y = '' #request.form.get("year")
#%%
x = db.execute("SELECT * FROM reviews").fetchall()
#%books \
#        where author like concat('%', concat(:auth,'%')) or \
#        title like concat('%', concat(:title,'%')) or \
#        isbn like concat('%', concat(:bn,'%') or \
#        year = :year order by year desc;", {"auth": au, "title": ti, "bn": bn, "year": y}).fetchall()
#%%
x = db.execute("select * from books where author like concat('%', concat(:auth,'%'))", {'auth' : au}).fetchall()
#%%
conds = ''
for p in [au, ti, bn, y]:
    if not p == :
#%%
A = [ z.user_id for z in x]
#%%
pms = { "key" : "TNDHWVNiRFkRMBueHIM3Bw", "isbns": "9781632168146" }
#%%
res = requests.get("https://www.goodreads.com/book/review_counts.json", params = pms).json()

#%%
res['books'][0]['average_rating']#.keys()#keys()#['average_rating']
#%%
z = db.execute("SELECT avg(rating) FROM reviews").fetchone()
#%%
db.execute("SELECT count(review) as ct FROM reviews WHERE isbn = :isbn_here", {"isbn_here" : b_isbn}).fetchone()
#%%
z = db.execute("SELECT id FROM users_test WHERE username = 'epfl'").fetchone()
#%%
z[0]