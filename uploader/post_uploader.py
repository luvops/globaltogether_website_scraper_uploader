import time
import traceback
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import TARGET_WRITE_URL, BOARD
from uploader.editor_utils import insert_image, imbed_youtube, cursor_to_end

# Upload post
def upload_post(driver, title, category, content):
    driver.get(TARGET_WRITE_URL.format(BOARD))
    time.sleep(1)

    # Wait then add title
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "post_subject")))
    title_input = driver.find_element(By.NAME, "post_subject")
    title_input.clear()
    title_input.send_keys(title)

    # Add category (if applicable)
    if category:
        category_dropdown = driver.find_element(By.NAME, "post_category")
        for option in category_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.text == category:
                option.click()
                break

    # Content (Froala Editor)
    editor = driver.find_element(By.CSS_SELECTOR, "div.fr-element.fr-view[contenteditable='true']")
    soup = BeautifulSoup(content, "html.parser")

    # Refined split preserving special tags within nested structure
    blocks = []
    for elem in soup.contents:
        if isinstance(elem, str):
            blocks.append(str(elem))
        elif elem.name in ["img", "table", "iframe"]:
            blocks.append(elem)
        elif isinstance(elem, BeautifulSoup):
            blocks.append(str(elem))
        else:
            specials = elem.find_all(["img", "table", "iframe"])
            if specials:
                html = str(elem)
                cursor = 0
                for special in specials:
                    special_html = str(special)
                    index = html.find(special_html, cursor)
                    if index > cursor:
                        blocks.append(html[cursor:index]) # append text before special tag
                    blocks.append(special) # append special tag
                    cursor = index + len(special_html)
                if cursor < len(html):
                    blocks.append(html[cursor:]) # append remaining text
            else:
                blocks.append(str(elem))

    # Process each block
    for block in blocks:
        if isinstance(block, str):  # Text block
            try:
                # Insert the text block into the editor
                driver.execute_script(
                    "arguments[0].insertAdjacentHTML('beforeend', arguments[1]);",
                    editor,
                    block
                )
                time.sleep(0.2)
            except Exception as e:
                print(f"[!] Failed to add text block: {e}")
                traceback.print_exc()
                continue
        elif block.name == "img":  # Handle <img> tags
            src = block.get("src", "")
            if src:
                try:
                    cursor_to_end(editor, driver)
                    insert_image(driver, src)
                except Exception as e:
                    print(f"[!] Failed to add image: {src} ({e})")
                    traceback.print_exc()
                    continue
        elif block.name == "table":  # Handle <table> tags
            try:
                table_html = str(block)  # Get the full HTML of the table
                driver.execute_script(
                    "arguments[0].insertAdjacentHTML('beforeend', arguments[1]);",
                    editor,
                    table_html
                )
            except Exception as e:
                print(f"[!] Failed to add table: {e}")
                traceback.print_exc()
                continue
        elif block.name == "iframe":  # Handle <iframe> tags (e.g., YouTube embeds)
            try:
                src = block.get("src", "")
                if src and "youtube.com" in src:
                    cursor_to_end(editor, driver)
                    imbed_youtube(driver, src)
            except Exception as e:
                print(f"[!] Failed to add YouTube video: {src} ({e})")
                traceback.print_exc()
                continue

    # Click submit button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Click confirm button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "CommonAlertModalButtonClose"))).click()

    time.sleep(2)