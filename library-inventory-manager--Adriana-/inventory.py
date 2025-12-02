# library_manager/inventory.py

import json
import logging
from pathlib import Path
from typing import List, Optional
from .book import Book

# ------------------------------
# LOGGING CONFIGURATION (TASK 5)
# ------------------------------
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class LibraryInventory:
    """
    Manages library books (add, search, display).
    Includes JSON persistence + logging + error handling.
    """

    def __init__(self, catalog_path: Path):
        self.catalog_path = Path(catalog_path)
        self.books: List[Book] = []
        self.load()

    # -----------------------------------
    # ADD BOOK
    # -----------------------------------
    def add_book(self, book: Book):
        self.books.append(book)
        self.save()
        logger.info(f"Book added: {book.title} (ISBN: {book.isbn})")

    # -----------------------------------
    # SEARCH METHODS
    # -----------------------------------
    def search_by_title(self, title: str):
        results = [b for b in self.books if title.lower() in b.title.lower()]
        logger.info(f"Searched by title: '{title}' — Matches: {len(results)}")
        return results

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        book = next((b for b in self.books if b.isbn == isbn), None)
        logger.info(f"Searched by ISBN: {isbn} — Found: {bool(book)}")
        return book

    # -----------------------------------
    # DISPLAY ALL BOOKS
    # -----------------------------------
    def display_all(self):
        return self.books

    # -----------------------------------
    # SAVE DATA (TASK 5)
    # -----------------------------------
    def save(self):
        try:
            self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
            data = [book.to_dict() for book in self.books]

            with open(self.catalog_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            logger.info("Catalog saved successfully. Total books: %d", len(self.books))

        except Exception as e:
            print("⚠️ Error saving catalog.json")
            logger.error(f"Failed to save catalog: {e}")

    # -----------------------------------
    # LOAD DATA (TASK 5)
    # -----------------------------------
    def load(self):
        if not self.catalog_path.exists():
            logger.warning("catalog.json not found. Creating a new file.")
            self.books = []
            self.save()
            return

        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.books = [Book(**item) for item in data]
            logger.info("Catalog loaded successfully with %d books.", len(self.books))

        except json.JSONDecodeError:
            print("⚠️ catalog.json is corrupted. Resetting file.")
            logger.error("catalog.json corrupted — creating a new one.")
            self.books = []
            self.save()

        except Exception as e:
            print("⚠️ Unexpected error loading catalog.json")
            logger.error(f"Unexpected load error: {e}")
            self.books = []