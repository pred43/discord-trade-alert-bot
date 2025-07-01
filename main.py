
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

DISCORD_EMAIL = os.getenv("DISCORD_EMAIL")
DISCORD_PASSWORD = os.getenv("DISCORD_PASSWORD")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

client = Client(TWILIO_SID, TWILIO_AUTH)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

def login_discord():
    driver.get("https://discord.com/login")
    time.sleep(3)
    driver.find_element(By.NAME, "email").send_keys(DISCORD_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(DISCORD_PASSWORD)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(8)

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
                            client.messages.create(
                                body=f"{author} ALERT:
{content}",
                                from_=TWILIO_FROM,
                                to=TWILIO_TO
                            )
                            alerted_messages.add(content)
            time.sleep(15)
        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    login_discord()
    monitor_messages()
