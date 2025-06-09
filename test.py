import os
import socket
import subprocess
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Settings ---
CHROME_PATH ="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHROME_DRIVER_PATH ="C:\\Users\\ameli\\Downloads\\chromedriver.exe"
PROMPT = (
    "You are an AI assistant helping me design "
    "a wide variety of high-converting Facebook/Instagram visual ads for my business, "
    "Mustard Seed Marketing. About Mustard Seed Marketing: We’re a Michigan-based ad agency"
    " helping service-based businesses (like home improvement, landscaping, medical, dental, trades, beauty) "
    "book more appointments and increase foot traffic through local Facebook and Instagram ads. Our tone is"
    " local, trustworthy, and results-driven — no fluff, no pressure, no long-term lock-ins. Design Instructions "
    "(alternate per output): Output a single, scroll-stopping visual ad. Always include the real Mustard Seed "
    "Marketing logo at the bottom or bottom right. Include a bold CTA button that says: CONTACT US. Use brand "
    "colors: dark green, mustard yellow, and neutral/beige tones. Use clean or slightly creative fonts — never "
    "overly decorative. Visual Style Rotation (for variety): Hyper-realistic photo backgrounds "
    "(e.g., workbenches, storefronts, phones, desks, tools). Flat or textured graphic layouts "
    "(e.g., paper backgrounds, chalkboard-style, speckled). Poster-style or taped-to-surface "
    "layouts (like flyers on real-world surfaces). Split layout: image on one side, message/CTA on the other."
    " Include effects like: tape corners, subtle crumples, lighting overlays, or shadows. Rotate Headline "
    "Themes (pain-based, benefit-based, urgent, local): Too many gaps in your schedule? Struggling to grow?"
    " We’ll bring customers to you. Tired of slow weeks? More calls. More jobs. Less stress. Get local leads "
    "without lifting a finger. You focus on your craft. We’ll bring the customers. We help Michigan businesses"
    " book more jobs — fast. Supporting text should be short, helpful, and persuasive. Always include: Your "
    "real logo. A bold, legible CTA: CONTACT US. Clear headline and short supporting text. Optional badges "
    "(include in some versions): 30-Day Satisfaction Guarantee. Michigan-Based Marketing Team. Month-to-Month Simplicity. "
    "Book More Jobs Fast. Generate one unique ad design per run — each with a visually distinct layout, message, "
    "and style."
)



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def find_free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def launch_chrome(port):
    args = [
        CHROME_PATH,
        f"--remote-debugging-port={port}",
        "--user-data-dir=C:\\Users\\ameli\\remote-profile",
        "--no-first-run",
        "--no-default-browser-check",
        "https://chat.openai.com"
    ]
    subprocess.Popen(args)
    logger.info("✅ Chrome launched. Please log in and complete human verification.")

def wait_for_login():
    while True:
        choice = input("Enter 'y' when done, or 'n' to keep waiting: ").strip().lower()
        if choice == 'y':
            break
        time.sleep(2)

def send_prompt(driver, promptt):
    try:
        logger.info("🔍 Waiting for ChatGPT prompt box...")
        wait = WebDriverWait(driver, 30)
        textarea = wait.until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
        driver.execute_script("arguments[0].focus();", textarea)

        textarea.clear()
        textarea.send_keys(promptt)

        # Add extra line break to simulate natural entry
        textarea.send_keys(Keys.SHIFT, Keys.ENTER)
        time.sleep(0.2)
        textarea.send_keys(Keys.SHIFT, Keys.ENTER)

        # Now actually submit
        textarea.send_keys(Keys.ENTER)

        logger.info("✅ Prompt sent (via real keypress).")
    except Exception as e:
        logger.exception("❌ Failed to send prompt: %s", e)


def main():
    port = find_free_port()
    launch_chrome(port)
    wait_for_login()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CHROME_PATH
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)
    driver.maximize_window()  # <-- Maximize the window here

    try:
        while True:
            send_prompt(driver, PROMPT)
            logger.info("⏳ Waiting 1 minutes before next prompt...")
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("🛑 Stopped by user.")
    finally:
        driver.quit()
        logger.info("✅ Browser closed.")

if __name__ == "__main__":
    main()
