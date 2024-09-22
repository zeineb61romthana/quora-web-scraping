import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Getting the URL to scrape
url = input('Enter the question you want to scrape-\n')
url = "https://www.quora.com/" + url.replace(" ", "-")

# Open the URL with Selenium
driver.get(url)

# Function to scroll the page and load more answers
def scroll_to_bottom(driver, pause_time=2, max_attempts=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempts = 0
    
    while attempts < max_attempts:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            attempts += 1
        else:
            attempts = 0  # Reset if new content loads
        
        last_height = new_height

# Scroll to the bottom to load more answers
scroll_to_bottom(driver, pause_time=3)

# Expand all "Read More" sections
read_more_buttons = driver.find_elements(By.CSS_SELECTOR, ".q-box.qu-mb--medium .q-click-wrapper")
for button in read_more_buttons:
    try:
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.5)
    except Exception as e:
        print(f"Error clicking read more: {e}")

# Extract the page source after all answers have loaded
page_source = driver.page_source

# Create a BeautifulSoup object for parsing
soup = BeautifulSoup(page_source, 'html.parser')

# Initialize the dictionary to store the scraped data
quora_json = dict()

# Extract the question title
question = soup.find("title")
quora_json["question"] = question.text.replace(" - Quora", "")

# Extract answers
quora_json["answers"] = []
answer_containers = soup.find_all("div", {"class": "q-box spacing_log_answer_content puppeteer_test_answer_content"})

for idx, container in enumerate(answer_containers):
    try:
        answer_text = container.get_text(separator="\n").strip()
        quora_json["answers"].append({"name": f"Answer {idx + 1}", "text": answer_text})
    except Exception as e:
        print(f"Error extracting answer {idx + 1}: {e}")

# Save the scraped data to a JSON file
with open('quora_data_selenium.json', 'w') as outfile:
    json.dump(quora_json, outfile, indent=4)

# Close the browser
driver.quit()

print(f"Scraped {len(quora_json['answers'])} answers.")
print("Data saved to quora_data_selenium.json.")
