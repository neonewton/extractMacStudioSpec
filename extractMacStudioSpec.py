#!/usr/bin/env python3


r"""
python3 -m venv .venv   
python3.11 -m venv .venv    
source .venv/bin/activate
.venv\Scripts\Activate.ps1
pip install selenium

MAC: open -a "Google Chrome" --args
--remote-debugging-port=9222
--user-data-dir="$HOME/chrome-debug-profile" then curl http://127.0.0.1:9222/json 

WINDOWS: 
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222 --user-data-dir="C:\Users\Neone\chrome-debug-profile" 
then 
curl http://127.0.0.1:9222/json

"""

import os

# Clear console
if os.name == "nt":        # Windows
    os.system("cls")
else:                      # Linux / macOS
    os.system("clear")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

KEYWORDS = [
    "Mac Studio Apple"
]

URL = "https://www.apple.com/sg-edu/shop/refurbished/mac/mac-studio"

# Setup
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 15)

driver.get(URL)
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ul/li')))

# Step 1: Collect matching product URLs with keywords and titles
product_info = []
items = driver.find_elements(By.XPATH, '//ul/li')

for item in items:
    try:
        title_elem = item.find_element(By.XPATH, './/h3/a')
        title = title_elem.text.strip()
        href = title_elem.get_attribute("href")

        for keyword in KEYWORDS:
            if keyword.lower() in title.lower() and href:
                product_info.append((keyword, title, href))
                break
    except:
        continue

# Step 2: Extract description per product
results = []
for keyword, title, link in product_info:
    try:
        driver.get(link)
        desc_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="content-:r9:-0"]/div/div/div[1]/div[2]/div'
        )))
        desc = desc_elem.text.strip()
        results.append((keyword, title, desc))
    except:
        continue

driver.quit()

# --- Step 3: Output ---
print("\n=== Extracted Product Descriptions ===")
for i, (keyword, title, description) in enumerate(results, 1):
    print(f"\n[{i}] {keyword}")
    print(f"Title: {title}")
    print(f"Description:\n{description}")
