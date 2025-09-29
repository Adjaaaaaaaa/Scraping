import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        """
        Cette fonction scrape la page d’accueil pour trouver toutes les catégories de livres.
        """
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
        """
        Cette fonction scrape toutes les pages d’une catégorie donnée.
        """
        category_name = response.meta["category"]

        for book in response.css("article.product_pod"):
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "availability": book.css("p.availability::text").re_first("\S+"),
                "rating": book.css("p.star-rating::attr(class)").get().split()[-1],
                "category": category_name,
            }

        # Pagination → continuer si page suivante
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_category,
                meta={"category": category_name}
            )
