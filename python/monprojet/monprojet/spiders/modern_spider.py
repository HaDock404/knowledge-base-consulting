import scrapy
from scrapy_playwright.page import PageMethod

class ModernSpider(scrapy.Spider):
    name = "modern_spider"
    allowed_domains = ["accteam.fr"]  # Remplace par ton domaine
    start_urls = ["https://www.accteam.fr/"]  # Remplace par un vrai site React

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60000,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),  # Attendre la fin des requêtes AJAX
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),  # Scroller
                        PageMethod("wait_for_timeout", 3000),  # Pause pour chargement du contenu
                    ],
                },
                callback=self.parse
            )

    def parse(self, response):
        titre = response.css("title::text").get()
        url = response.url
        texte = " ".join(response.xpath("//body//text()").getall()).strip()

        yield {"url": url, "titre": titre, "texte": texte}

        # Suivre les liens internes
        for lien in response.css("a::attr(href)").getall():
            if lien.startswith("http") or lien.startswith("/"):
                yield response.follow(lien, meta={"playwright": True}, callback=self.parse)
