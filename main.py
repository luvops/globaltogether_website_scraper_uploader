from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config import *
from scraper.post_list import get_post_links
from scraper.post_content import scrape_post
from uploader.login import admin_login
from uploader.post_uploader import upload_post

def main():
    options = Options()
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        print("[*] Logging in...")
        admin_login(driver, ADMIN_ID, ADMIN_PW)

        print(f"[+] Scraping page {PAGE}...")
        post_urls = get_post_links(TABLE, PAGE)

        for url in post_urls:
            print(f"    ⬇ Scraping: {url}")
            title, category, content = scrape_post(url)

            print(f"    ⬆ Uploading: {title[:30]}...")
            upload_post(driver, title, category, content)

    finally:
        driver.quit()
        print("[✓] Task complete.")

if __name__ == "__main__":
    main()