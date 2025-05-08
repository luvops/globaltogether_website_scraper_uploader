import requests
from bs4 import BeautifulSoup
from config import GTGT_BOARD_URL

# Fetch URLs of the posts
def get_post_links(table_num, page_num):
    links = []
    for page in range(1, int(page_num) + 1):
        url = GTGT_BOARD_URL.format(table_num, page)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # Try gallery-style layout
        gallery_found = False
        for li in soup.select("li.gall_li"):
            post_link_tag = li.select_one("li.gall_text_href a[href*='wr_id=']")
            if post_link_tag:
                href = post_link_tag.get("href")
                if href:
                    links.append(href)
                    gallery_found = True

        # If not gallery format, try traditional layout
        if not gallery_found:
            for a in soup.select("td.td_subject a, div.txt_area a"):
                href = a.get("href")
                if href and "wr_id=" in href:
                    links.append(href)

    links.reverse()
    return links