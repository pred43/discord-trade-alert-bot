import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # ✅ Needed for Keys.RETURN
from twilio.rest import Client
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Environment Variables
DISCORD_EMAIL = os.getenv("DISCORD_EMAIL")
DISCORD_PASSWORD = os.getenv("DISCORD_PASSWORD")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

# ✅ Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH)

# ✅ Selenium options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# ✅ Set up driver
driver = webdriver.Chrome(options=options)

# ✅ Login function
def login_discord(driver):
    driver.get("https://discord.com/login")
    time.sleep(3)

    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")

    email_input.send_keys(DISCORD_EMAIL)
    password_input.send_keys(DISCORD_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # wait for login to complete

# ✅ Monitor function
def monitor_messages():
    alerted_messages = set()
    while True:
        try:
            messages = driver.find_elements(By.CSS_SELECTOR, "[class^='message-']")
            for msg in messages[-10:]:
                author_elements = msg.find_elements(By.CSS_SELECTOR, "h3")
                if not author_elements:
                    continue
                author = author_elements[0].text
                content = msg.text.upper()
                if author and ("BRANDO" in author.upper() or "SHOOF" in author.upper()):
                    if "BOUGHT" in content or "SOLD" in content:
                        if content not in alerted_messages:
                            body = f"{author} ALERT: {content}"
                            message = client.messages.create(
                                body=body,
                                from_=TWILIO_FROM,
                                to=TWILIO_TO
                            )
                            alerted_messages.add(content)
            time.sleep(15)
        except Exception as e:
            print("Error:", e)
            time.sleep(10)

# ✅ Main entry point
if __name__ == "__main__":
    login_discord(driver)
    monitor_messages()
