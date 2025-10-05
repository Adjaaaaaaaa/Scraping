from sqlalchemy.orm import Session
from sqlalchemy import and_
from books_api.data.tables import BookTable
from books_scraper.books_scraper.models import Book, BookHistory



class BookRepository:
    """
    Repository class for querying BookTable in the database.
    
    Provides methods to retrieve books with various filters.
    """
    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy session object
        """
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        """
        Retrieve all books with pagination.
        
        Args:
            skip (int): Number of records to skip
            limit (int): Maximum number of records to return
        
        Returns:
            List[BookTable]: List of books
        """       
        return self.db.query(BookTable).offset(skip).limit(limit).all()


    def get_by_upc(self, upc: str):
        """
        Retrieve a book by its UPC code.
        
        Args:
            upc (str): The UPC of the book
        
        Returns:
            BookTable or None: Book record if found
        """
        return self.db.query(BookTable).filter(BookTable.upc == upc).first()


    def get_by_category(self, category: str):
        """
        Retrieve books by category.
        
        Args:
            category (str): Category name
        
        Returns:
            List[BookTable]: Books in the given category
        """
        return self.db.query(BookTable).filter(BookTable.category == category).all()

    def get_by_price_range(self, min_price: float, max_price: float):
        """
        Retrieve books within a specific price range.
        
        Args:
            min_price (float): Minimum price
            max_price (float): Maximum price
        
        Returns:
            List[BookTable]: Books matching the price criteria
        """
        return self.db.query(BookTable).filter(
            and_(BookTable.price >= min_price, BookTable.price <= max_price)
        ).all()

    def get_by_availability(self, availability: str):
        """
        Retrieve books by availability status.
        
        Args:
            availability (str): e.g., "In stock" or "Out of stock"
        
        Returns:
            List[BookTable]: Books matching the availability
        """
        return self.db.query(BookTable).filter(BookTable.availability == availability).all()

   
    def search(self, category=None, min_price=0, max_price=10000, availability=None, skip=0, limit=100, rating=None):
        """
        Retrieve books using multiple optional filters.
        
        Args:
            category (str, optional): Filter by category
            min_price (float, optional): Minimum price
            max_price (float, optional): Maximum price
            availability (str, optional): Filter by availability
            skip (int, optional): Number of records to skip
            limit (int, optional): Maximum number of records to return
            rating (int, optional): Filter by book rating
        
        Returns:
            List[BookTable]: Books matching the combined filters
        """
        query = self.db.query(BookTable)
        
        if category:
            query = query.filter(BookTable.category == category)
        
        if availability:
            query = query.filter(BookTable.availability == availability)
        
        if rating:
            query = query.filter(BookTable.rating == rating)  # filtre par rating
        
        query = query.filter(BookTable.price >= min_price, BookTable.price <= max_price)
        return query.offset(skip).limit(limit).all()
    



class BookHistoryRepository:
    """
    Repository class for querying BookHistory table.
    
    Provides methods to retrieve historical changes for books, 
    especially price changes.
    """
    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        
        Args:
            db (Session): SQLAlchemy session object
        """
        self.db = db

    def get_price_changes(self, book_upc: str):
        """
        Retrieve only price change history for a specific book.
        
        Args:
            book_upc (str): The UPC code of the book
        
        Returns:
            List[dict]: List of price change events with old/new prices and date
        """
        all_history = (
            self.db.query(BookHistory)
            .filter(BookHistory.book_upc == book_upc)
            .order_by(BookHistory.change_date.asc())
            .all()
        )

        price_changes = []
        for h in all_history:
            old_price = h.old_data.get("price") if h.old_data else None
            new_price = h.new_data.get("price") if h.new_data else None
            if old_price != new_price:
                price_changes.append({
                    "change_date": h.change_date,
                    "old_price": old_price,
                    "new_price": new_price,
                    "action": h.action
                })
        return price_changes
