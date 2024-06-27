# SeleniumBaseScraper

This respository is a "helper" for other scraper repositories.

- Provides functions to get your scraper up to speed such as:

  - create_browser() # Creates a chromium browser directed at your desired url.
  - read_data() # Get information from a web element via it's Xpath.
  - click_button() # Navigate to a button via it's Xpath, and click it.

- Miscellaneous functions include:
  - formatting numbers to or from a $ format (helpful with scraping financial websites)
  - Date utilities, to add, subtract, or compare dates (helpful with scraping finacial statements)

### Setup

1. Clone the repository:
   `git clone https://github.com/PrimalFinance/SeleniumBaseScraper.git`

2. Import `SeleniumBaseScraper` to your scraper.

```
    from SeleniumBaseScraper.scraper import SeleniumBaseScraper


    class ExampleScraper(SeleniumBaseScraper):
        def __init__(self):
            super().__init__("Path to Chromedriver")
```
