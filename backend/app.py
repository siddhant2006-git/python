from datetime import datetime
import json
import os

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "library_data.json")

app = Flask(__name__)
CORS(app)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


@app.route("/api/books", methods=["GET"])
def get_books():
    query = request.args.get("query", "").strip().lower()
    books = load_data()
    if query:
        books = [
            book
            for book in books
            if query in book["title"].lower() or query in book["author"].lower()
        ]
    return jsonify(books)


@app.route("/api/books", methods=["POST"])
def add_book():
    payload = request.get_json() or {}
    book_id = payload.get("book_id", "").strip().upper()
    title = payload.get("title", "").strip().title()
    author = payload.get("author", "").strip().title()

    if not book_id or not title or not author:
        abort(400, description="book_id, title, and author are required")

    books = load_data()
    if any(book["book_id"] == book_id for book in books):
        abort(400, description="Book ID already exists")

    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "is_issued": False,
        "issued_to": None,
        "issue_date": None,
    }
    books.append(new_book)
    save_data(books)
    return jsonify(new_book), 201


@app.route("/api/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_data()
    book_id = book_id.strip().upper()
    filtered = [book for book in books if book["book_id"] != book_id]
    if len(filtered) == len(books):
        abort(404, description="Book not found")
    save_data(filtered)
    return jsonify({"message": "Book deleted"})


@app.route("/api/books/<book_id>/issue", methods=["PUT"])
def issue_return_book(book_id):
    payload = request.get_json() or {}
    action = payload.get("action")
    borrower = payload.get("borrower", "").strip().title()

    if action not in {"issue", "return"}:
        abort(400, description="Action must be 'issue' or 'return'")

    books = load_data()
    for book in books:
        if book["book_id"] == book_id.strip().upper():
            if action == "issue":
                if book["is_issued"]:
                    abort(400, description="Book is already issued")
                if not borrower:
                    abort(400, description="Borrower name is required to issue a book")
                book["is_issued"] = True
                book["issued_to"] = borrower
                book["issue_date"] = datetime.now().strftime("%Y-%m-%d")
            else:
                if not book["is_issued"]:
                    abort(400, description="Book is not currently issued")
                book["is_issued"] = False
                book["issued_to"] = None
                book["issue_date"] = None
            save_data(books)
            return jsonify(book)

    abort(404, description="Book not found")


@app.route("/api/books/<book_id>", methods=["GET"])
def get_book(book_id):
    books = load_data()
    for book in books:
        if book["book_id"] == book_id.strip().upper():
            return jsonify(book)
    abort(404, description="Book not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
