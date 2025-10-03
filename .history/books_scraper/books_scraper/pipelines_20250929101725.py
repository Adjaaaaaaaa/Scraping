import re
from sqlalchemy.orm import sessionmaker
from models import Book, engine

# Dictionnaire pour convertir les notes en chiffres
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# Session pour communiquer avec SQLite
Session = sessionmaker(bind=engine)

class CleanBooksPipeline:
    def process_item(self, item, spider):
        # Nettoyer prix (£51.77 → 51.77)
        item["price"] = float(re.sub(r"[^\d.]", "", item["price"]))

        # Convertir rating (ex: "Three" → 3)
        item["rating"] = RATINGS.get(item["rating"], 0)

        # Nettoyer disponibilité
        item["availability"] = "In stock" if "In" in item["availability"] else "Out of stock"

        return item


class SaveBooksPipeline:
    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        # Sauvegarde en BDD SQLite
        book = Book(**item)
        self.session.add(book)
        return item
