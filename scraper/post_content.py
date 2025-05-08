import requests
from bs4 import BeautifulSoup

# Fetch post title, date, category, content
def scrape_post(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Extract title
    title = soup.select_one("#bo_v_title").text.strip()

    # Check category and modify title accordingly
    category = None
    if title.startswith("해외사업"):
        title = title[7:]
        category = "해외사업"
    elif title.startswith("국내사업"):
        title = title[7:]
        category = "국내사업"
    elif title.startswith("해외후기"):
        title = title[7:]
        category = "해외후기"
    elif title.startswith("국내후기"):
        title = title[7:]
        category = "국내후기"
    elif title.startswith("기타후기"):
        title = title[7:]
        category = "기타후기"
    elif title.startswith("기타"):
        title = title[5:]
        category = "기타"

    # Extract content
    content_elem = soup.select_one("#bo_v_con")
    content_html = content_elem.decode_contents().strip()

    # Prepend relavant link to the content
    link_section = soup.select_one("#bo_v_link")
    related_link = ''
    if link_section:
        strong_tag = link_section.find("strong")
        if strong_tag:
            related_link = strong_tag.text.strip()
    if related_link:
        content_html = f"Link: <p>{related_link}</p>" + content_html

    # Extract date from .view_info strong tag
    date_text = ''
    info_section = soup.select_one("#bo_v_info")
    if info_section:
        strong_tags = info_section.find_all("strong")
        if len(strong_tags) >= 2:
            date_text = strong_tags[1].text.strip()

    # Prepend the date to the content
    if date_text:
        content_html = f"<p>{date_text}</p>" + content_html
    
    # Extract Author
    author = ''
    author_section = soup.select_one(".sv_guest")
    if author_section:
        author = author_section.text.strip()
    if author:
        content_html = f"<p>작성자: {author}</p>" + content_html

    return title, category, content_html