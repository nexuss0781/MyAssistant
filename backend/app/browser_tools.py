
import asyncio
from playwright.async_api import async_playwright, Page, expect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserTools:
    def __init__(self):
        self.browser = None
        self.page = None

    async def initialize(self):
        if self.browser is None:
            logger.info("Initializing Playwright browser...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            logger.info("Playwright browser initialized.")

    async def close(self):
        if self.browser:
            logger.info("Closing Playwright browser...")
            await self.browser.close()
            await self.playwright.stop()
            self.browser = None
            self.page = None
            logger.info("Playwright browser closed.")

    async def navigate_to_url(self, url: str) -> str:
        """Navigates the browser to the specified URL."""
        await self.initialize()
        try:
            logger.info(f"Navigating to {url}")
            await self.page.goto(url)
            return f"Successfully navigated to {url}"
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return f"Error navigating to {url}: {e}"

    async def get_page_content(self) -> str:
        """Returns the full HTML content of the current page."""
        await self.initialize()
        return await self.page.content()

    async def extract_text(self) -> str:
        """Extracts all visible text content from the current page."""
        await self.initialize()
        return await self.page.evaluate("document.body.innerText")

    async def extract_markdown(self) -> str:
        """Extracts the main content of the current page and converts it to Markdown."""
        await self.initialize()
        # This is a placeholder. A real implementation would use a library like `html2text`
        # or a more sophisticated parsing approach to convert HTML to Markdown.
        # For now, we'll just return the innerText as a simplified representation.
        logger.warning("Markdown extraction is a simplified implementation (innerText).")
        return await self.page.evaluate("document.body.innerText")

    async def click_element(self, selector: str) -> str:
        """Clicks an element identified by a CSS selector."""
        await self.initialize()
        try:
            logger.info(f"Clicking element with selector: {selector}")
            await self.page.click(selector)
            return f"Clicked element: {selector}"
        except Exception as e:
            logger.error(f"Error clicking element {selector}: {e}")
            return f"Error clicking element {selector}: {e}"

    async def fill_form_field(self, selector: str, value: str) -> str:
        """Fills a form field identified by a CSS selector with the given value."""
        await self.initialize()
        try:
            logger.info(f"Filling field {selector} with value: {value}")
            await self.page.fill(selector, value)
            return f"Filled field {selector} with value: {value}"
        except Exception as e:
            logger.error(f"Error filling field {selector}: {e}")
            return f"Error filling field {selector}: {e}"

    async def take_screenshot(self, path: str = "screenshot.png") -> str:
        """Takes a screenshot of the current page and saves it to the specified path."""
        await self.initialize()
        try:
            logger.info(f"Taking screenshot to {path}")
            await self.page.screenshot(path=path)
            return f"Screenshot saved to {path}"
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return f"Error taking screenshot: {e}"

    async def web_search(self, query: str) -> str:
        """Performs a web search using a search engine (e.g., Google) and returns the results page URL."""
        await self.initialize()
        try:
            search_url = f"https://www.google.com/search?q={query}"
            logger.info(f"Performing web search for '{query}' at {search_url}")
            await self.page.goto(search_url)
            return f"Navigated to search results for '{query}'. Use get_page_content or extract_text to view results."
        except Exception as e:
            logger.error(f"Error performing web search for '{query}': {e}")
            return f"Error performing web search for '{query}': {e}"

# Example usage (for testing purposes)
async def main():
    browser_tools = BrowserTools()
    try:
        print(await browser_tools.navigate_to_url("https://www.example.com"))
        print(await browser_tools.extract_text()[:200]) # Print first 200 chars
        print(await browser_tools.take_screenshot("example.png"))
        print(await browser_tools.web_search("playwright python"))
        print(await browser_tools.take_screenshot("playwright_search.png"))
    finally:
        await browser_tools.close()

if __name__ == "__main__":
    asyncio.run(main())

