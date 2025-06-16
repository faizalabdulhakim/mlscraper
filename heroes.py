import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import csv

options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    options=options,
)

driver.get("https://www.mobilelegends.com/hero")


WebDriverWait(driver, 5).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)

# wait up to 5 seconds on loading
wait_policy_btn = WebDriverWait(driver, 5).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mt-cb-policy-close"))
)

wait_yes_cookies_btn = WebDriverWait(driver, 5).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div#mt-cb-p"))
)

close_policy_btn = driver.find_element(By.CSS_SELECTOR, "div.mt-cb-policy-close")
close_policy_btn.click()

cookies_yes_btn = driver.find_element(By.CSS_SELECTOR, "div#mt-cb-p")
cookies_yes_btn.click()

wait_load_heroes = WebDriverWait(driver, 5).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mt-list-layout"))
)

wait_heroes = WebDriverWait(driver, 5).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".mt-list-layout .mt-list-item .mt-text span"))
)

# get the initial scroll height
# find the scrollable container
scroll_container = driver.find_element(By.CSS_SELECTOR, ".mt-list-layout")

# get initial scroll height
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

while True:
    # scroll to the bottom of the scrollable container
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

    # wait for new content to load
    time.sleep(5)

    # get new height
    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

    # break if no more new content
    if new_height == last_height:
        break

    last_height = new_height

heroes = driver.find_elements(By.CSS_SELECTOR, ".mt-list-layout .mt-list-item")

result = []
for hero in heroes:
    name = hero.find_element(By.CSS_SELECTOR, ".mt-text span").text
    img = hero.find_element(By.CSS_SELECTOR, ".mt-image img")

    # Scroll image into view to trigger lazy loading
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)

    # Wait for 'src' to be non-empty
    WebDriverWait(driver, 10).until(
        lambda d: img.get_attribute("src") and "data:image" not in img.get_attribute("src")
    )

    image_url = img.get_attribute("src")

    result.append(dict(name=name, image=image_url))

# with open('heroes.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=2)

with open('heroes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["name", "image"])
    writer.writeheader()
    writer.writerows(result)


driver.quit()