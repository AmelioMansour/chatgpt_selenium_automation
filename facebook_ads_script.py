from chatgpt_selenium_automation.handler import ChatGPTAutomation

# Define the path where the chrome driver is installed on your computer
chrome_driver_path = r"C:\Users\ameli\Downloads\chromedriver.exe"
# the sintax r'"..."' is required because the space in "Program Files" in the chrome path
chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'

# Create an instance
chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)

# Define a prompt and send it to chatgpt
prompt = "What are the benefits of exercise?"
chatgpt.send_prompt_to_chatgpt(prompt)

# Retrieve the last response from ChatGPT
response = chatgpt.return_last_response()
print(response)

# Save the conversation to a text file
file_name = "conversation.txt"
chatgpt.save_conversation(file_name)

# Close the browser and terminate the WebDriver session
chatgpt.quit()