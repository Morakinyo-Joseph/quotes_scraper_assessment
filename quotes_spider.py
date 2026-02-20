import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes_data.json',
        'DOWNLOAD_DELAY': 0.5, # 500ms delay to be polite to the server
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In-memory cache to avoid scraping the same author page multiple times
        self.author_cache = {}

    def parse(self, response):
        """Parses the main quote pages and handles pagination."""
        quotes = response.css('div.quote')
        
        for quote in quotes:
            # Extract standard quote data
            quote_text = quote.css('span.text::text').get()
            author_name = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            author_url = quote.css('span a::attr(href)').get()

            quote_data = {
                'quote_text': quote_text,
                'author_name': author_name,
                'tags': tags
            }

            # Check cache before yielding a new request
            if author_name in self.author_cache:
                # We already scraped this author; merge the cached data and yield
                yield {**quote_data, **self.author_cache[author_name]}
            else:
                # We haven't seen this author yet; follow the link
                yield response.follow(
                    author_url,
                    callback=self.parse_author,
                    cb_kwargs={'quote_data': quote_data, 'author_name': author_name}
                )

        # Handle Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response, quote_data, author_name):
        """Parses the author profile pages and merges data."""
        author_data = {
            'author_full_name': response.css('h3.author-title::text').get(default='').strip(),
            'date_of_birth': response.css('span.author-born-date::text').get(),
            'place_of_birth': response.css('span.author-born-location::text').get()
        }

        # Store the scraped author data in our cache
        self.author_cache[author_name] = author_data

        # Merge the original quote data with the new author data and yield
        yield {**quote_data, **author_data}