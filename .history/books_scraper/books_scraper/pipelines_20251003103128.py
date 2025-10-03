import re
from datetime import datetime
from .models import Book, BookHistory, Session

# Conversion des notes textuelles en chiffres
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class CleanBooksPipeline:
    def process_item(self, item, spider):
        # Nettoyage du prix principal
        item["price"] = float(re.sub(r"[^\d.]", "", str(item["price"])))

        # Nettoyage des champs prix/taxe
        for key in ["price_excl_tax", "price_incl_tax", "tax"]:
            if key in item and item[key] is not None:
                item[key] = float(re.sub(r"[^\d.]", "", str(item[key])))

        # Conversion rating
        item["rating"] = RATINGS.get(item.get("rating", ""), 0)

        # Disponibilité
        item["availability"] = "In stock" if "In" in item.get("availability", "") else "Out of stock"

        # Copies disponibles
        if "copies_available" in item and item["copies_available"]:
            item["copies_available"] = int(item["copies_available"])

        # Nombre de reviews
        if "num_reviews" in item and item["num_reviews"]:
            item["num_reviews"] = int(item["num_reviews"])

        return item


class SaveBooksPipeline:
    def open_spider(self, spider):
        self.session = Session()
        self.scraped_upcs = set()

    def close_spider(self, spider):
        # Supprime les livres qui ne sont plus présents
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
        self.scraped_upcs.add(item["upc"])
        book = self.session.query(Book).filter_by(upc=item["upc"]).first()
        old_data = None

        if book:
            # Vérifie s’il y a un changement
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
            # Nouveau livre
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
