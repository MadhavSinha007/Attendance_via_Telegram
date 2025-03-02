import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

# Telegram Bot API token and chat ID
TELEGRAM_API_TOKEN = '' #use your telegram api token
CHAT_ID = '' #use your chat_id

# URL for login
login_url = "https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp"
element_to_click_xpath = "//a[@id='listId9']"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")  # Start maximized
    chrome_options.add_argument("--window-size=1920,1080")  # Set specific window size
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    return webdriver.Chrome(options=chrome_options)

def take_full_screenshot(driver):
    # Get the total height of the page
    total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    
    # Set window size to capture everything
    driver.set_window_size(1920, total_height)
    
    # Wait for any animations to complete
    time.sleep(2)
    
    # Take screenshot
    screenshot = driver.get_screenshot_as_png()
    return screenshot

def send_telegram_message(message, image_path=None):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(telegram_url, data=payload)
    if response.status_code == 200:
        print("Message sent to Telegram bot")
    else:
        print("Failed to send message to Telegram bot")
    
    if image_path:
        send_image_to_telegram(image_path)

def send_image_to_telegram(image_path):
    image_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
    }
    files = {'photo': open(image_path, 'rb')}
    response = requests.post(image_url, data=payload, files=files)
    if response.status_code == 200:
        print("Image sent to Telegram bot")
    else:
        print("Failed to send image to Telegram bot")

def fetch_updates(offset=None):
    updates_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/getUpdates"
    if offset:
        updates_url += f"?offset={offset}"
    response = requests.get(updates_url)
    return response.json()

def main():
    last_update_id = None
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)  # Create a WebDriverWait instance

    try:
        # Load login page and wait for it to be ready
        driver.get(login_url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "col-sm-4")))

        # Get CAPTCHA
        captcha_element = driver.find_element(By.CLASS_NAME, "col-sm-4")
        captcha_screenshot = captcha_element.screenshot_as_png
        captcha_pil = Image.open(io.BytesIO(captcha_screenshot))
        captcha_code = pytesseract.image_to_string(captcha_pil)
        print("CAPTCHA code:", captcha_code)

        # Fill login form
        wait.until(EC.presence_of_element_located((By.NAME, "login")))
        driver.find_element(By.NAME, "login").send_keys("") #enter your user id (srm)
        driver.find_element(By.NAME, "passwd").send_keys("") #enter your pass-code
        driver.find_element(By.NAME, "ccode").send_keys(captcha_code.strip())

        # Click login and wait for navigation
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-custom') and contains(@class, 'btn-user') and contains(@class, 'btn-block') and contains(@onclick, 'funLogin()')]")))
        login_button.click()

        # Wait for the element to be clickable after login
        element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click_xpath)))
        element_to_click.click()
        
        # Wait for page to load completely
        time.sleep(5)

        while True:
            updates = fetch_updates(offset=last_update_id)
            if updates["result"]:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    message_text = update["message"]["text"]
                    chat_id = update["message"]["chat"]["id"]

                    if message_text.lower() == "hi":
                        # Take screenshot with proper waiting
                        screenshot = take_full_screenshot(driver)
                        screenshot_path = "full_page_screenshot.png"
                        
                        with open(screenshot_path, "wb") as f:
                            f.write(screenshot)

                        print("Full page screenshot captured after receiving 'hi' message")
                        message = "Screenshot captured after receiving 'hi' message."
                        send_telegram_message(message, screenshot_path)

            time.sleep(10)

    except Exception as e:
        print("Error:", e)
        send_telegram_message(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()