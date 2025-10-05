import re
from datetime import datetime
from .models import Book, BookHistory
from .database import SessionLocal, init_db
"""
Scrapy pipelines for cleaning and saving book data.

- CleanBooksPipeline: Cleans and normalizes scraped data.
- SaveBooksPipeline: Saves data to SQLite and tracks history of changes.
"""
# Mapping textual ratings to integers
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class CleanBooksPipeline:
    """
    Pipeline to clean and normalize scraped book data before saving.

    - Converts prices and tax fields to float
    - Converts textual ratings to integer
    - Standardizes availability
    - Extracts number of copies and reviews
    - Fills missing string fields with empty strings
    """
    def process_item(self, item, spider):
        # MAIN PRICE
        if "price" in item and item["price"]:
            item["price"] = float(re.sub(r"[^\d.]", "", str(item["price"])))

        # PRICE / TAX FIELDS 
        for key in ["price_excl_tax", "price_incl_tax", "tax"]:
            if key in item and item[key] is not None:
                item[key] = float(re.sub(r"[^\d.]", "", str(item[key])))

        # RATING 
        if "rating" in item:
            if isinstance(item["rating"], str):
                # Extraction depuis le texte si nécessaire
                rating_word = item["rating"].split()[-1]
                item["rating"] = RATINGS.get(rating_word, 0)
          
        # AVAILABILITY  
        if "availability" in item and item["availability"]:
            avail_text = str(item["availability"])
            item["availability"] = "In stock" if "In" in avail_text else "Out of stock"

        # COPIES AVAILABLE 
        if "copies_available" in item and item["copies_available"]:
            # Extrait juste le nombre (ex: "In stock (22 available)")
            match = re.search(r"\d+", str(item["copies_available"]))
            item["copies_available"] = int(match.group()) if match else 0
        else:
            item["copies_available"] = 0

        # NUMBER OF REVIEWS 
        if "num_reviews" in item and item["num_reviews"]:
            item["num_reviews"] = int(item["num_reviews"])
        else:
            item["num_reviews"] = 0

        # OTHER STRING FIELDS
        for key in ["title", "category", "url", "upc"]:
            if key in item and item[key] is None:
                item[key] = ""

        return item


class SaveBooksPipeline:
    """
    Pipeline to save cleaned book data to the database and track history.

    - Adds new books
    - Updates existing books and logs old/new data
    - Deletes missing books and logs the deletion
    """
    def open_spider(self, spider):
        """Initialize database connection and session."""
        init_db()
        self.session = SessionLocal()
        self.scraped_upcs = set()

    def close_spider(self, spider):
        """Handle deletion of books not found in the latest scrape."""
        all_books = self.session.query(Book).all()
        for book in all_books:
            if book.upc not in self.scraped_upcs:
                history = BookHistory(
                    book_upc=book.upc,
                    action="deleted",
                    old_data={col.name: getattr(book, col.name) for col in Book.__table__.columns},
                    new_data=None,
                    change_date=datetime.utcnow()
                )
                self.session.add(history)
                self.session.delete(book)
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        """
        Add or update a book record in the database and log changes.

        Args:
            item (dict): Cleaned book data
            spider (scrapy.Spider): Current spider instance

        Returns:
            dict: The processed item
        """
        self.scraped_upcs.add(item["upc"])
        book = self.session.query(Book).filter_by(upc=item["upc"]).first()
        old_data = None

        if book:
            # Check for changes in existing book
            old_data = {col.name: getattr(book, col.name) for col in Book.__table__.columns}
            changed = any(old_data.get(k) != item.get(k) for k in item)
            if changed:
                history = BookHistory(
                    book_upc=book.upc,
                    action="updated",
                    old_data=old_data,
                    new_data=item.copy(),
                    change_date=datetime.utcnow()
                )
                self.session.add(history)
                for key, value in item.items():
                    setattr(book, key, value)
        else:
            # New book, add to database and history
            book = Book(**item)
            self.session.add(book)
            history = BookHistory(
                book_upc=item["upc"],
                action="added",
                old_data=None,
                new_data=item.copy(),
                change_date=datetime.utcnow()
            )
            self.session.add(history)

        self.session.commit()
        return item
