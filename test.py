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
    "You are an AI assistant helping me design high-converting visual ads for my business, Mustard Seed Marketing."
    "About the Business:"
    "Mustard Seed Marketing is a local digital advertising agency based in Michigan. We help service-based businesses book more appointments and increase foot traffic using Facebook and Instagram ads. Our tone is local, trustworthy, and results-driven — no fluff, no pressure, no contracts."
    "Ad Requirements:"
    "- Each output should be a single Facebook/Instagram-ready visual ad."
    "- Use my real logo (I will upload it) — place it cleanly at the bottom or bottom right."
    "- Use my brand colors: dark green, mustard yellow, and neutral/beige tones."
    "- Fonts should be clean or slightly creative — never overly decorative."
    "- Always include a bold CTA button that says: CONTACT US."
    "- Headline must stand out and be pain- or benefit-based."
    "- Supporting text should be short and helpful."
    "- Use a balanced, professional layout."
    "Visual Style Instructions:"
    "- Prioritize **hyper-realistic photograph-style backgrounds** (e.g., local storefronts, tools, workbenches, handwritten notes, busy shops, mobile phones, etc.)."
    "- Alternate occasionally with flat or textured graphic design (clean paper, speckled textures)."
    "- Include occasional poster-style ads (as if pinned, taped, or displayed on real surfaces)."
    "- Use distressed or curved fonts for emotional/pain-based headlines."
    "Sample Message Themes (rotate between):"
    "- 'Too Many Gaps In Your Schedule?'"
    "- 'Having a Hard Time Growing?'"
    "- 'Not Getting Enough Clients?'"
    "- 'Want More Customers?'"
    "- 'Let’s Grow Your Business Online.'"
    "- 'We Help Michigan Businesses Book More Jobs Fast.'"
    ""
    "Final Output Must:"
    "- Look professional and eye-catching on social media."
    "- Include legible text."
    "- Feature the logo."
    "- Include the CTA button saying CONTACT US."
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
