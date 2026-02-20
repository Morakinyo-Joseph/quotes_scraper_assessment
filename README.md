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