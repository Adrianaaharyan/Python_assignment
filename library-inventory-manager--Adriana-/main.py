# cli/main.py

import logging
from pathlib import Path

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

# Ensure logs directory exists and configure logging (safe if inventory has already configured it)
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def print_menu():
    print("\n============================")
    print("   LIBRARY MAIN MENU")
    print("============================")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    print("============================")


def add_book(inventory):
    print("\n--- Add New Book ---")
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()

    if not title or not author or not isbn:
        print("❌ All fields are required.")
        return

    if inventory.search_by_isbn(isbn):
        print("❌ A book with this ISBN already exists.")
        return

    book = Book(title, author, isbn)
    inventory.add_book(book)
    logger.info(f"Book added via CLI: {title} (ISBN: {isbn})")
    print("✅ Book added successfully!")


def issue_book(inventory):
    print("\n--- Issue Book ---")
    isbn = input("Enter ISBN to issue: ").strip()

    book = inventory.search_by_isbn(isbn)
    if not book:
        print("❌ Book not found.")
        return

    if book.issue():
        inventory.save()
        logger.info(f"Book issued via CLI: {isbn}")
        print("✅ Book issued successfully!")
    else:
        print("❌ Book is already issued.")


def return_book(inventory):
    print("\n--- Return Book ---")
    isbn = input("Enter ISBN to return: ").strip()

    book = inventory.search_by_isbn(isbn)
    if not book:
        print("❌ Book not found.")
        return

    if book.return_book():
        inventory.save()
        logger.info(f"Book returned via CLI: {isbn}")
        print("✅ Book returned successfully!")
    else:
        print("❌ Book is already available.")


def view_books(inventory):
    print("\n--- All Books in Library ---")
    books = inventory.display_all()

    if not books:
        print("Library is empty.")
        return

    for book in books:
        print(book)


def search_book(inventory):
    print("\n--- Search Book ---")
    print("1. By Title")
    print("2. By ISBN")

    choice = input("Choose option: ").strip()

    if choice == "1":
        title = input("Enter title keyword: ").strip()
        results = inventory.search_by_title(title)

        if results:
            print("\n--- Results ---")
            for b in results:
                print(b)
        else:
            print("❌ No books found.")

    elif choice == "2":
        isbn = input("Enter ISBN: ").strip()
        book = inventory.search_by_isbn(isbn)

        if book:
            print("\n--- Book Found ---")
            print(book)
        else:
            print("❌ No book found with that ISBN.")

    else:
        print("❌ Invalid choice.")


def run():
    inventory = LibraryInventory(Path("data/catalog.json"))

    try:
        while True:
            print_menu()
            choice = input("Enter choice: ").strip()

            if choice == "1":
                add_book(inventory)
            elif choice == "2":
                issue_book(inventory)
            elif choice == "3":
                return_book(inventory)
            elif choice == "4":
                view_books(inventory)
            elif choice == "5":
                search_book(inventory)
            elif choice == "6":
                print("Exiting program. Goodbye!")
                logger.info("Program exited by user.")
                break
            else:
                print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted (Ctrl+C). Exiting safely.")
        logger.warning("Program interrupted by user.")


if __name__ == "__main__":
    run()

