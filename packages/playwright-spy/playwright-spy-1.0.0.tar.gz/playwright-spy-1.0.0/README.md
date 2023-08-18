# playwright-spy [![GitHub Workflow Status](https://img.shields.io/badge/playwright-python-8A2BE2)

> A plugin for [playwright-python](https://img.shields.io/badge/just%20the%20message-8A2BE2) to prevent detection.

<p align="center"><img src="https://i.imgur.com/q2xBjqH.png" /></p>

## Install

```bash
pip install playwright-spy
```

## Usage

```python
from playwright.sync_api import sync_playwright
import playwright_spy

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    playwright_spy.load_sync(page)
    page.goto("https://bot.sannysoft.com/")
    page.screenshot(path="example.png", full_page=True)
    browser.close()
```
