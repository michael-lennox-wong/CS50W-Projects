import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgres://wgoeytjfrbnypa:e41b67b7351067f3d6f059fd6e16879e8a1d643e8a78da68b9a4399e7cfdf20e@ec2-54-228-243-238.eu-west-1.compute.amazonaws.com:5432/d5fsnhhq7lj4g4")
db = scoped_session(sessionmaker(bind=engine))


f = open("C:\\Users\\micha\\Documents\\GitHub\\First-Web-Projects\\project1\\books.csv")
reader = csv.reader(f)
next(reader) #We skip the first line in the file as there is a header
for bn, t, a, y in reader:
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
               {"isbn": bn, "title": t, "author": a, "year": y})
    print(f"Added {t} by {a} to database")
db.commit()
