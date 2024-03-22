#
# Created on Mon Jul 25 2023
#
# Copyright (c) 2023 ym
#
# !pip install playwright

from playwright.sync_api import sync_playwright, expect
import re

cookies = "cookies.json"

def login():
    with sync_playwright() as pw:
        # start browser and open a new tab
        browser = pw.firefox.launch(headless=False)
        context = browser.new_context(viewport={"width": 1080, "height": 760})
        page = context.new_page()
        page.goto("https://civitai.com/login?returnUrl=/")
        # page.goto("https://civitai.com")

        # page.wait_for_url("https://civitai.com")
        expect(page).to_have_url(re.compile("civitai.com+/$"), timeout=5000*1e3)
        # expect(page.get_by_role("link").filter(
        #             has=page.get_by_text(re.compile("Featured Images", re.IGNORECASE))
        #             )).to_be_visible(timeout=5000*1e3)
        storage = context.storage_state(path=cookies)
        print("saved cookies")

if __name__=="__main__":
    login()
