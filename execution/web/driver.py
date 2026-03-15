from playwright.async_api import async_playwright


class PlaywrightDriver:
    _instance = None

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = PlaywrightDriver()
            await cls._instance._start()
        
        # Check if browser is still alive
        if not cls._instance.browser.is_connected():
            await cls._instance._start()
            
        return cls._instance

    async def _start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def navigate(self, url: str):
        await self.page.goto(url)
        await self.page.wait_for_timeout(2000)

    async def get_page(self):
        return self.page

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        PlaywrightDriver._instance = None
