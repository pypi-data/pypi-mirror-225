import importlib.resources

from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


__all__ = ['load_sync', 'load_async']

SCRIPT = importlib.resources.read_text(package=__package__, resource="spy.min.js")


def load_sync(page: SyncPage):
    """teaches synchronous playwright Page to be stealthy like a ninja!"""
    page.add_init_script(SCRIPT)


async def load_async(page: AsyncPage):
    """teaches asynchronous playwright Page to be stealthy like a ninja!"""
    await page.add_init_script(SCRIPT)
