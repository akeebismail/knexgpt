from firecrawl import Firecrawl

class WebScraper:
    """Class for web scraping using Firecrawl."""
    
    def __init__(self):
        self.firecrawl = Firecrawl()
    
    def scrape_url(self, url: str) -> str:
        """Scrape the content of the given URL.
        
        Args:
            url: The URL to scrape.
        
        Returns:
            The scraped content as a string.
        """
        return self.firecrawl.scrape(url) 