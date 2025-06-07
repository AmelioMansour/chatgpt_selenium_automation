from chatgpt_selenium_automation.handler import ChatGPTAutomation
import time

# Path to chromedriver executable
chrome_driver_path = r"C:\Users\ameli\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Path to Chrome executable - adjust if yours is different
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'

chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

first_prompt = "Generate a hyper realistic Facebook ad for mustard seed marketing."
chatgpt.send_prompt_to_chatgpt(first_prompt)

# Wait 1.5 minutes before sending the second prompt
print("Waiting 1.5 minutes before sending the next prompt...")

for _ in range(10):
    time.sleep(1)

second_prompt = "Generate another hyper realistic Facebook ad for mustard seed marketing."
chatgpt.send_prompt_to_chatgpt(second_prompt)

chatgpt.quit()
