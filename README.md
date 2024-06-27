# SeleniumBaseScraper

This respository is a "helper" for other scraper repositories.

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
