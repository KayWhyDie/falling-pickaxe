# filepath: c:\Users\KWD\Documents\GitHub\falling-pickaxe\src\selenium_chat.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
def poll_live_chat_messages_selenium(youtube_url, poll_interval=10):
    """
    Indefinitely poll live chat messages from a YouTube live stream using Selenium.
    Yields up to 10 new user messages per poll.
    Args:
        youtube_url (str): The URL of the YouTube live stream.
        poll_interval (int): Seconds between polls.
    Yields:
        list of dict: Each dict contains 'author', 'message', 'photo'.
    """
    options = Options()
    # options.add_argument("--headless")  # Uncomment for headless
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get(youtube_url)
    time.sleep(10)  # Wait for page to load
    try:
        chatframe = driver.find_element(By.CSS_SELECTOR, "iframe#chatframe")
        driver.switch_to.frame(chatframe)
    except Exception as e:
        print("Could not find chat iframe:", e)
        driver.quit()
        return
    seen = set()
    try:
        while True:
            chat_items = driver.find_elements(By.TAG_NAME, "yt-live-chat-text-message-renderer")
            new_messages = []
            for item in chat_items:
                try:
                    author = item.find_element(By.ID, "author-name").text
                    message = item.find_element(By.ID, "message").text
                    try:
                        photo_elem = item.find_element(By.CSS_SELECTOR, "#author-photo img")
                        photo_url = photo_elem.get_attribute("src")
                    except Exception:
                        photo_url = None
                    key = (author, message, photo_url)
                    if key not in seen:
                        seen.add(key)
                        msg = {"author": author, "message": message, "photo": photo_url}
                        new_messages.append(msg)
                except Exception:
                    continue
            if new_messages:
                # Only yield up to 10 unique user messages per poll
                yield new_messages[:10]
    finally:
        driver.quit()
    return messages