import scrapy
import re

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        categories = response.css("div.side_categories ul li ul li a")
        for category in categories:
            category_name = category.css("::text").get().strip()
            category_url = response.urljoin(category.attrib["href"])
            yield response.follow(
                category_url,
                callback=self.parse_category,
                meta={"category": category_name}
            )

    def parse_category(self, response):
        category_name = response.meta["category"]

        for book in response.css("article.product_pod"):
            book_url = response.urljoin(book.css("h3 a::attr(href)").get())
            yield response.follow(
                book_url,
                callback=self.parse_book,
                meta={"category": category_name}
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_category,
                meta={"category": category_name}
            )

    def parse_book(self, response):
        category_name = response.meta["category"]
        title = response.css("div.product_main h1::text").get()
        price = response.css("p.price_color::text").get()
        availability_text = response.css("p.availability::text").getall()
        availability = "".join(availability_text).strip()

        # Nombre de copies disponibles
        match = re.search(r"\((\d+) available\)", availability)
        copies_available = int(match.group(1)) if match else None

# Récupérer le rating (étoiles)     
        rating_class = response.css("p.star-rating").attrib.get("class", "")
        match = re.search(r"star-rating (\w+)", rating_class)
        rating_text = match.group(1) if match else None
        RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = RATINGS.get(rating_text, 0)
            

        # UPC
        upc = response.css("table.table.table-striped tr:nth-child(1) td::text").get()
        # Prix hors taxe, TTC, taxe
        price_excl_tax = response.css("table.table.table-striped tr:nth-child(3) td::text").get()
        price_incl_tax = response.css("table.table.table-striped tr:nth-child(4) td::text").get()
        tax = response.css("table.table.table-striped tr:nth-child(5) td::text").get()
        # Nombre de reviews
        num_reviews = response.css("table.table.table-striped tr:nth-child(7) td::text").get()

        yield {
            "title": title,
            "category": category_name,
            "price": price,
            "availability": availability,
            "copies_available": copies_available,
            "upc": upc,
            "price_excl_tax": price_excl_tax,
            "price_incl_tax": price_incl_tax,
            "tax": tax,
            "num_reviews": num_reviews,
            "url": response.url,
        }