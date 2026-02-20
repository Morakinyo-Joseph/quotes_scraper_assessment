# Python Web Scraping Assessment: Quotes to Scrape

This repository contains the solution for the web scraping take-home assessment. The objective is to extract quotes, tags, and author metadata from [Quotes to Scrape](https://quotes.toscrape.com/) while handling pagination and nested page navigation.

## Prerequisites & Execution

The scraper is built using **Scrapy**. To keep the evaluation process simple, I designed it as a standalone script rather than a multi-file Scrapy project. 

**Requirements:**
* Python 3.8+
* Scrapy (`pip install scrapy`)

**To run the scraper and generate the data:**
```bash
scrapy runspider quotes_spider.py
```

**1. Overall Approach**

I chose Scrapy for this task over standard requests and BeautifulSoup. While the latter is fine for simple scripts, Scrapy is a production-grade framework built for asynchronous spidering, which is highly beneficial when dealing with nested page navigation (joining quote data with author profile data).

To demonstrate best practices, the script includes built-in politeness measures:

- Auto-throttling: A 500ms DOWNLOAD_DELAY is implemented to respect the target server's resources.

- User-Agent: A standard browser User-Agent is passed in the headers to prevent basic bot-blocking.

**2. Pagination and Navigation**

Pagination: Pagination is handled dynamically within the main parse method. The scraper looks for the "Next" button using the CSS selector li.next a::attr(href). If the element exists, the spider yields a recursive response.follow request back to the parse method until it reaches the last page.

Navigation (Author Profiles): To collect the author data, the spider extracts the relative link to the author's bio for every quote. It then yields a request to that URL, calling a secondary parser (parse_author). To maintain a flat, relational data structure, the initial quote data is passed to the author request using Scrapy's cb_kwargs. The secondary parser extracts the author's birth details, merges the two dictionaries, and yields the final, complete item.

**3. Challenge Encountered & Addressed**

The Challenge: The website features multiple quotes from the same authors (e.g., Albert Einstein appears on almost every page). Out of the box, following every author link would result in the scraper fetching Einstein's bio page dozens of times, which wastes bandwidth, slows down the crawl, and puts unnecessary load on the server.

The Solution: I implemented an in-memory cache (self.author_cache) within the Spider. Before yielding a request to an author's profile, the script checks if that author has already been scraped. If they are in the cache, the script instantly merges the cached author data with the new quote data and yields the item, completely bypassing the redundant HTTP request.

**4. Improvement With More Time**

If I were deploying this into a true production environment, I would make the following improvements:

- Data Validation: I would implement Pydantic models or Scrapy Item Loaders to strictly validate the data types and handle missing fields more gracefully before the data reaches the export pipeline.

- Persistent Caching: I would move the in-memory author cache to a persistent storage layer (like Redis or DiskCache). This way, if the spider is paused and restarted, or run incrementally on a cron job, it retains the memory of previously visited authors across multiple execution runs.
