#
# Created on Mon Jul 25 2023
#
# Copyright (c) 2023 rlsn
#
# !pip install playwright

import re, os
import pprint
import asyncio
from playwright.async_api import async_playwright, expect
import os, json, argparse
from collections import defaultdict
cookies = "cookies.json"


async def download_models(urls,dir=".",cookies="cookies.json"):
    results={}
    os.makedirs(dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        try:
            context = await browser.new_context(storage_state=cookies)
            print("loaded cookies")
        except:
            context = await browser.new_context()
        page = await context.new_page()
        # page = await browser.new_page()

        downloads = []
        finished = 0
        for ui,url in enumerate(urls):
            print(f"visiting {url}")
            await page.goto(url)
            # await page.screenshot(path="screenshot.png") # debug with this line
            async with page.expect_download() as download_info:
                # locate download link
                try:
                    await page.get_by_role("link", name=re.compile("Download.*", re.IGNORECASE)).click(timeout=6000)
                    # link = await page.locator("xpath=/html/body/div[1]/div/div/div/main/div[1]/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/a/div").click(timeout=6000)
                except:
                    print("looking for alternative link")
                    try:
                        await page.locator("xpath=/html/body/div[1]/div/div/div/main/div[1]/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/button[2]/div").click(timeout=6000)
                        link = await page.locator("xpath=/html/body/div[1]/div/div/div/main/div[1]/div[2]/div/div[3]/div[1]/div/div[2]/div[1]/div[1]/div").click(timeout=6000)
                    except:
                        print(f"cannot find download link for {url}, pass")
                        continue
            download = await download_info.value

            print(f"downloading: {download.suggested_filename}: {download.url}")
            words = await page.get_by_role("row").filter(
                    has=page.get_by_text(re.compile("trigger words", re.IGNORECASE))
                    ).all_inner_texts()
            try:
                words = words[0].lower().replace("trigger words","").strip().replace("\n",",")
                results[download.suggested_filename] = words
                print(f"retrieved trigger words: {words}")
            except:
                results[download.suggested_filename] = ""
                print(f"no trigger words found")
                
            if os.path.exists(f"{dir}/{download.suggested_filename}"):
                await download.cancel()
                finished+=1
                print(f"Already downloaded. Done {finished}/{len(urls)}")
                continue

            downloads.append(download)
        

        for download in downloads:
            await download.path()
            await download.save_as(f"{dir}/{download.suggested_filename}")
            finished+=1
            print(f"Done {finished}/{len(urls)}")
        await browser.close()
    return results

async def get_titles(urls,cookies="cookies.json"):
    results=defaultdict()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            context = await browser.new_context(storage_state=cookies)
            print("loaded cookies")
        except:
            context = await browser.new_context()
        page = await context.new_page()

        for ui,url in enumerate(urls):
            await page.goto(url)
            name = await page.get_by_role("heading").all_inner_texts()
            results[name[0]] = url
            print(f"{url} : {name[0]}")

    with open("model_info.json",'w') as fp:
        json.dump(results, fp, indent=4, ensure_ascii=False)
    return results

def read_urls(file):
    with open(file,"r") as f:
        urls = [u.strip() for u in f.readlines()]
    return urls

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_file', type=str, help="file containing the urls you are interested", default="urls.txt")
    parser.add_argument('--download_dir', type=str, help="the directory where the downloaded files are located", default="./downloads")

    parser.add_argument('--info', action='store_true', help="get title of the urls", default=None)
    parser.add_argument('--download', action='store_true', help="run example match with lastest moddel")

    args = parser.parse_args()
    urls=read_urls(args.url_file)
    if args.info:
        asyncio.run(get_titles(urls,cookies))
    elif args.download:
        asyncio.run(download_models(urls,dir=args.download_dir,cookies=cookies))

