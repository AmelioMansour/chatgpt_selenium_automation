import logging
from chatgpt_selenium_automation.handler import ChatGPTAutomation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chrome_driver_path = r"C:\Users\ameli\Downloads\chromedriver.exe"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

chatgpt = None
try:
    chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

    prompt = "What are the benefits of exercise?"
    chatgpt.send_prompt_to_chatgpt(prompt)

    response = chatgpt.return_last_response()
    print(response)

    file_name = "conversation.txt"
    chatgpt.save_conversation(file_name)
except Exception as exc:
    logger.exception("Script execution failed: %s", exc)
finally:
    if chatgpt:
        chatgpt.quit()
