import json
import os
from datetime import datetime


DATA_FILE ="LIBARY01.json"
# save file and load reload
def load_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_file(data):
  with open(DATA_FILE,"w") as file :
    json.dump(data,file,indent=4)

# admin login
def login():
  print("\n ----admin login----")
  username=input("enter the username :")
  password=input("enter the password")
  if username == "siddhant bhatnagar"and password == "krish@1234":
    print("login successfully ")
    return True 
  else:
    print("invalid pass word ")
    return False

# add book
def add_book(books):
    print("\n --enter the book--")
    book_id = input("enter the book_id ").strip().upper()
    if any(book["book_id"] == book_id for book in books):
        print("the book wil be exists now  ")
        return
    book_title = input("enter the title of the book ")
    book_author = input("enter author ")

    new_book = {
        "book_id": book_id,
        "book_title": book_title,
        "book_author": book_author,
        "is_issued": False,
        "issued_to": None,
        "issue_date": None,
    }
    books.append(new_book)
    save_file(books)
    print("f successful`{book_title}` add the libary")

# delete book
def delete_book(books):
  print("\n enter the book id ")
  book_id=input("enter the book id ")
  for book in books :
    if book["book_id"]==book_id:
      books.remove(book)
      save_file(books)
      print("successfully delete `{book_title}` book delete ")

def search_book(books):
   print("\n enter the search id")
   query=input("enter the book id :").strip().upper()

   found_book=[book for book in books if query in book["book_title"].upper() or query in book["book_author"] ]



