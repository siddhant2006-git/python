import json
import os
from datetime import datetime

DATA_FILE = "library_data.json"


# --- STEP 2: Save and Load Records ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --- STEP 3: Admin Login ---
def admin_login():
    print("\n--- Admin Login ---")
    username = input("Username: ")
    password = input("Password: ")
    if username == "admin" and password == "admin123":
        print("Login successful!\n")
        return True
    else:
        print("Invalid credentials. Access denied.\n")
        return False


# --- STEP 4: Add Book ---
def add_book(books):
    print("\n--- Add New Book ---")
    book_id = input("Enter Book ID (e.g., B001): ").strip().upper()

    # Check if ID already exists
    if any(book["book_id"] == book_id for book in books):
        print("Error: Book ID already exists!")
        return

    title = input("Enter Book Title: ").strip().title()
    author = input("Enter Author Name: ").strip().title()

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
    print(f"Success: '{title}' added to the library.")


# --- STEP 5: Delete Book ---
def delete_book(books):
    print("\n--- Delete Book ---")
    book_id = input("Enter Book ID to delete: ").strip().upper()

    for book in books:
        if book["book_id"] == book_id:
            books.remove(book)
            save_data(books)
            print(f"Success: Book '{book['title']}' deleted.")
            return

    print("Error: Book ID not found.")


# --- STEP 6: Search Book ---
def search_book(books):
    print("\n--- Search Book ---")
    query = input("Enter title or author to search: ").strip().lower()

    found_books = [
        book
        for book in books
        if query in book["title"].lower() or query in book["author"].lower()
    ]

    if found_books:
        print(f"\nFound {len(found_books)} result(s):")
        for book in found_books:
            status = "Issued" if book["is_issued"] else "Available"
            print(
                f"ID: {book['book_id']} | Title: {book['title']} | Author: {book['author']} | Status: {status}"
            )
    else:
        print("No books found matching your search.")


# --- STEP 7: Issue Book ---
def issue_book(books):
    print("\n--- Issue Book ---")
    book_id = input("Enter Book ID to issue: ").strip().upper()

    for book in books:
        if book["book_id"] == book_id:
            if book["is_issued"]:
                print(
                    f"Error: '{book['title']}' is already issued to {book['issued_to']}."
                )
            else:
                borrower = input("Enter borrower's name: ").strip().title()
                book["is_issued"] = True
                book["issued_to"] = borrower
                book["issue_date"] = datetime.now().strftime("%Y-%m-%d")
                save_data(books)
                print(f"Success: '{book['title']}' issued to {borrower}.")
            return

    print("Error: Book ID not found.")


# --- STEP 8: Return Book ---
def return_book(books):
    print("\n--- Return Book ---")
    book_id = input("Enter Book ID to return: ").strip().upper()

    for book in books:
        if book["book_id"] == book_id:
            if not book["is_issued"]:
                print(f"Error: '{book['title']}' is not currently issued.")
            else:
                book["is_issued"] = False
                book["issued_to"] = None
                book["issue_date"] = None
                save_data(books)
                print(f"Success: '{book['title']}' has been returned.")
            return

    print("Error: Book ID not found.")


# --- STEP 9: Main Menu ---
def main():
    if not admin_login():
        return  # Exit if login fails

    books = load_data()

    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. View All Books")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            delete_book(books)
        elif choice == "3":
            issue_book(books)
        elif choice == "4":
            return_book(books)
        elif choice == "5":
            search_book(books)
        elif choice == "6":
            print("\n--- All Books ---")
            if not books:
                print("Library is empty.")
            else:
                for book in books:
                    status = "Issued" if book["is_issued"] else "Available"
                    print(
                        f"ID: {book['book_id']} | {book['title']} by {book['author']} | {status}"
                    )
        elif choice == "7":
            print("Saving data and exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
