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
def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load the page
        time.sleep(pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # If the scroll height doesn't change, we've reached the bottom
        last_height = new_height

# Scroll to the bottom to load more answers
scroll_to_bottom(driver, pause_time=3)

# Extract the page source after all answers have loaded
page_source = driver.page_source

# Create a BeautifulSoup object for parsing
soup = BeautifulSoup(page_source, 'html.parser')

# Initialize the dictionary to store the scraped data
quora_json = dict()

# Extract the question title
question = soup.find("title")
quora_json["question"] = question.text.replace(" - Quora", "")

# Find all answer sections based on a more accurate div container (adjust based on the HTML structure)
quora_json["answers"] = []

# Updated method to extract full answer content
answer_containers = soup.find_all("div", {"class": "q-box spacing_log_answer_content puppeteer_test_answer_content"})

# Loop through each answer container and extract the text
for idx, container in enumerate(answer_containers):
    answer_text = container.get_text(separator="\n").strip()
    # Store the answer with a label 'Answer 1', 'Answer 2', etc.
    quora_json["answers"].append({"name": f"Answer {idx + 1}", "text": answer_text})

# Save the scraped data to a JSON file
with open('quora_data_selenium.json', 'w') as outfile:
    json.dump(quora_json, outfile, indent=4)

# Close the browser
driver.quit()

print(f"Scraped {len(quora_json['answers'])} answers.")
print("Data saved to quora_data_selenium.json.")
