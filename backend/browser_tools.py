
import asyncio
from playwright.async_api import async_playwright, Page

class BrowserTools:
    def __init__(self):
        self.browser = None
        self.page = None

    async def _ensure_browser_page(self):
        if not self.browser or not self.page:
            pw = await async_playwright().start()
            self.browser = await pw.chromium.launch(headless=True)
            self.page = await self.browser.new_page()

    async def navigate_to_url(self, url: str) -> str:
        await self._ensure_browser_page()
        await self.page.goto(url)
        return f"Navigated to {url}"

    async def web_search(self, query: str) -> str:
        await self._ensure_browser_page()
        # This is a simplified example. A real web search would involve a search engine.
        # For now, let's just navigate to a search result page if a URL is provided.
        # Or, if it's a query, we'd use a search API or a pre-defined search engine URL.
        search_url = f"https://www.google.com/search?q={query}"
        await self.page.goto(search_url)
        return f"Performed web search for '{query}'. Current URL: {self.page.url}"

    async def extract_content(self, content_type: str = "text") -> str:
        await self._ensure_browser_page()
        if content_type == "text":
            return await self.page.inner_text('body')
        elif content_type == "markdown":
            # This is a placeholder. Converting HTML to Markdown is complex.
            # A dedicated library would be needed here.
            return f"Markdown conversion not fully implemented. Extracted text: {await self.page.inner_text('body')}"
        elif content_type == "html":
            return await self.page.content()
        else:
            return "Unsupported content type. Choose 'text', 'markdown', or 'html'."

    async def interact_with_element(self, selector: str, action: str, value: str = None) -> str:
        await self._ensure_browser_page()
        if action == "click":
            await self.page.click(selector)
            return f"Clicked element with selector: {selector}"
        elif action == "fill":
            if value is None:
                return "Value must be provided for 'fill' action."
            await self.page.fill(selector, value)
            return f"Filled element with selector '{selector}' with value '{value}'"
        else:
            return "Unsupported interaction action. Choose 'click' or 'fill'."

    async def take_screenshot(self, path: str = "screenshot.png") -> str:
        await self._ensure_browser_page()
        await self.page.screenshot(path=path)
        return f"Screenshot saved to {path}"

    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None

# Example usage (for testing purposes)
async def main():
    browser_tools = BrowserTools()
    print(await browser_tools.navigate_to_url("https://www.example.com"))
    print(await browser_tools.extract_content("text"))
    await browser_tools.close()

if __name__ == "__main__":
    asyncio.run(main())

