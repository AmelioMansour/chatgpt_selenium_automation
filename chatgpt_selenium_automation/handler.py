import os
import socket
import subprocess
import threading
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ChatGPTAutomation:
    def __init__(self, chrome_path, chrome_driver_path):
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = "https://chat.openai.com"
        free_port = self.find_available_port()
        logger.debug("Using free port %s for remote debugging", free_port)

        try:
            self.launch_chrome_with_remote_debugging(free_port)
            self.wait_for_human_verification()
            self.driver = self.setup_webdriver(free_port)
            self.driver.get(url)
            self.cookie = self.get_cookie()
        except Exception as exc:
            logger.exception("Initialization failed: %s", exc)
            raise

    @staticmethod
    def find_available_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            port = s.getsockname()[1]
            logger.debug("Found available port %s", port)
            return port

    def launch_chrome_with_remote_debugging(self, port):
        def open_chrome():
            chrome_cmd = [
        self.chrome_path,
        f'--remote-debugging-port={port}',
        '--user-data-dir=C:\\Users\\ameli\\remote-profile',
        '--no-first-run',
        '--no-default-browser-check',
        'https://chat.openai.com'  # <- THIS will open ChatGPT immediately
    ]

            logger.debug("Launching Chrome with: %s", chrome_cmd)
            subprocess.Popen(chrome_cmd)

        try:
            chrome_thread = threading.Thread(target=open_chrome)
            chrome_thread.start()
            time.sleep(3)
        except Exception as exc:
            logger.exception("Could not launch Chrome: %s", exc)
            raise

    def setup_webdriver(self, port):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = self.chrome_path
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        try:
            driver = webdriver.Chrome(service=Service(self.chrome_driver_path), options=chrome_options)
            logger.debug("WebDriver connected to Chrome on port %s", port)
            return driver
        except Exception as exc:
            logger.exception("Error setting up WebDriver: %s", exc)
            raise

    def get_cookie(self):
        try:
            cookies = self.driver.get_cookies()
            cookie = [elem for elem in cookies if elem["name"] == '__Secure-next-auth.session-token'][0]['value']
            logger.debug("Session cookie successfully retrieved")
            return cookie
        except Exception as exc:
            logger.exception("Failed to get session cookie: %s", exc)
            raise

    def send_prompt_to_chatgpt(self, prompt):
        try:
            input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@id, "prompt-textarea")]')
            self.driver.execute_script(f"arguments[0].value = '{prompt}';", input_box)
            input_box.send_keys(Keys.RETURN)
            logger.debug("Prompt sent: %s", prompt)
            self.check_response_ended()
        except Exception as exc:
            logger.exception("Error sending prompt: %s", exc)
            raise

    def check_response_ended(self):
        start_time = time.time()
        try:
            while len(self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')[-1].find_elements(
                    by=By.CSS_SELECTOR, value='button.text-token-text-tertiary')) < 1:
                time.sleep(0.5)
                if time.time() - start_time > 60:
                    logger.debug("Timed out waiting for response")
                    break
            time.sleep(1)
        except Exception as exc:
            logger.exception("Error while waiting for response to finish: %s", exc)
            raise

    def return_chatgpt_conversation(self):
        try:
            elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
            logger.debug("Conversation elements found: %d", len(elements))
            return elements
        except Exception as exc:
            logger.exception("Failed to retrieve conversation: %s", exc)
            raise

    def save_conversation(self, file_name):
        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        try:
            with open(os.path.join(directory_name, file_name), "a") as file:
                for i in range(0, len(chatgpt_conversation), 2):
                    file.write(
                        f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 1].text}\n\n{delimiter}\n\n")
            logger.debug("Conversation saved to %s", file_name)
        except Exception as exc:
            logger.exception("Failed to save conversation: %s", exc)
            raise

    def return_last_response(self):
        try:
            response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
            if not response_elements:
                logger.debug("No response elements located")
                return ""
            last = response_elements[-1].text
            logger.debug("Last response retrieved")
            return last
        except Exception as exc:
            logger.exception("Failed to retrieve last response: %s", exc)
            raise

    @staticmethod
    def wait_for_human_verification():
        logger.debug("Prompting user for manual verification")
        print("You need to complete login or human verification in the browser.")

        while True:
            try:
                user_input = input("Enter 'y' once done, or 'n' to keep waiting: ").lower().strip()
            except EOFError as exc:
                logger.exception("Input error during verification wait: %s", exc)
                raise

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def quit(self):
        logger.debug("Closing the browser and quitting WebDriver")
        print("Closing the browser...")
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as exc:
            logger.exception("Error during quit: %s", exc)
            raise
