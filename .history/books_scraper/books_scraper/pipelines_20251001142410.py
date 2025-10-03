import re         # regex, inclus dans Python → pas besoin d'installer
from sqlalchemy.orm import sessionmaker
from .models import Book, engine
from .models import Book, BookHistory, Session
from datetime import datetime

# Dictionnaire pour convertir les notes en chiffres
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# Session pour communiquer avec SQLite
Session = sessionmaker(bind=engine)

class CleanBooksPipeline:
    def process_item(self, item, spider):
        # Nettoyer prix (£51.77 → 51.77)
        item["price"] = float(re.sub(r"[^\d.]", "", str(item["price"])))

        # Nettoyer price_excl_tax, price_incl_tax, tax
        for key in ["price_excl_tax", "price_incl_tax", "tax"]:
            if key in item:
                item[key] = re.sub(r"[^\d.]", "", str(item[key]))

        # Convertir rating (ex: "Three" → 3)
        if "rating" in item:
            item["rating"] = RATINGS.get(item["rating"], 0)
        else:
            item["rating"] = 0

        # Nettoyer disponibilité
        item["availability"] = "In stock" if "In" in item["availability"] else "Out of stock"

        # Nettoyer copies_available
        if "copies_available" in item and item["copies_available"] is not None:
            item["copies_available"] = int(item["copies_available"])

        # Nettoyer num_reviews
        if "num_reviews" in item and item["num_reviews"] is not None:
            item["num_reviews"] = int(item["num_reviews"])

        return item


class SaveBooksPipeline:
    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        session = Session()
        scraped_upcs = set(self.scraped_upcs)  # à remplir dans process_item
        all_books = session.query(Book).all()
        for book in all_books:
            if book.upc not in scraped_upcs:
                history = BookHistory(
                    book_upc=book.upc,
                    action="deleted",
                    old_data={col.name: getattr(book, col.name) for col in Book.__table__.columns},
                    new_data=None,
                    change_date=datetime.utcnow()
                )
                session.add(history)
                session.delete(book)
        session.commit()
        session.close()

from .models import Book, BookHistory, Session
from datetime import datetime

class SaveBooksPipeline:
    def process_item(self, item, spider):
        session = Session()
        book = session.query(Book).filter_by(upc=item["upc"]).first()
        action = None
        old_data = None

        if book:
            # Compare tous les champs
            old_data = {col.name: getattr(book, col.name) for col in Book.__table__.columns}
            new_data = item.copy()
            # Si changement, enregistre l’historique
            if any(old_data.get(k) != new_data.get(k) for k in new_data):
                action = "updated"
                history = BookHistory(
                    book_upc=book.upc,
                    action=action,
                    old_data=old_data,
                    new_data=new_data,
                    change_date=datetime.utcnow()
                )
                session.add(history)
            # Met à jour le livre
            for key, value in item.items():
                setattr(book, key, value)
        else:
            # Nouveau livre
            book = Book(**item)
            session.add(book)
            action = "added"
            history = BookHistory(
                book_upc=item["upc"],
                action=action,
                old_data=None,
                new_data=item.copy(),
                change_date=datetime.utcnow()
            )
            session.add(history)

        session.commit()
        session.close()
        return item

