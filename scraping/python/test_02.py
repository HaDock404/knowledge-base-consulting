import scrapy

class SiteSpider(scrapy.Spider):
    name = "site_spider"
    allowed_domains = ["hadock404.github.io"]  # Remplace par le domaine du site
    start_urls = ["https://hadock404.github.io/app-web-me/"]  # Remplace par l’URL du site de départ

    def parse(self, response):
        # Extraction du titre de la page
        titre = response.css('title::text').get()
        url = response.url
        yield {"url": url, "titre": titre}

        # Extraction des liens internes et suivi de la navigation
        for lien in response.css("a::attr(href)").getall():
            if lien.startswith("http") or lien.startswith("/"):
                yield response.follow(lien, callback=self.parse)
