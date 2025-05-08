import time
from selenium.webdriver.common.by import By

# Insert image into Froala editor
def insert_image(driver, src):
    image_button = driver.find_element(By.ID, "insertImage-1")
    image_button.click()
    imageByUrl_button = driver.find_element(By.ID, "imageByURL-1")
    imageByUrl_button.click()
    imageUrl_input = driver.find_element(By.ID, "fr-image-by-url-layer-text-1")
    imageUrl_input.clear()
    imageUrl_input.send_keys(src)
    driver.find_element(By.CSS_SELECTOR, "button.fr-command.fr-submit[data-cmd='imageInsertByURL']").click()
    time.sleep(3)

# Insert video into Froala editor
def imbed_youtube(driver, url):
    youtube_button = driver.find_element(By.ID, "insertVideo-1")
    youtube_button.click()
    youtubeUrl_input = driver.find_element(By.ID, "fr-video-by-url-layer-text-1")
    youtubeUrl_input.clear()
    youtubeUrl_input.send_keys(url)
    driver.find_element(By.CSS_SELECTOR, "button.fr-command.fr-submit[data-cmd='videoInsertByURL']").click()
    time.sleep(3)

# Move cursor to the end of the Froala editor
def cursor_to_end(editor, driver):
    driver.execute_script("""
        var editor = arguments[0];
        var range = document.createRange();
        var sel = window.getSelection();
        range.selectNodeContents(editor);
        range.collapse(false); // Collapse to the end
        sel.removeAllRanges();
        sel.addRange(range);
    """, editor)