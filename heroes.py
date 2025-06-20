import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import csv

import os

import requests
START_FROM_ID = 1
END_ID = 129

def download_image(url, file_path, file_name):
    fullpath = os.path.join(file_path, file_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(fullpath, 'wb') as out_file:
            out_file.write(response.content)
    else:
        print(f"Failed to download {url}")


def format_name(name):
    return name.lower().replace(".", "_").replace(" ", "_").replace("-", "_").replace("'", "").replace(":", "")

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
# options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    options=options,
)

driver.get("https://www.mobilelegends.com/hero")

# ============ START WAIT READY ============
WebDriverWait(driver, 5).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)

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
# ============ END WAIT READY ============

# ============ START SCROLL ============
scroll_container = driver.find_element(By.CSS_SELECTOR, ".mt-list-layout")
last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)

    time.sleep(2)

    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_container)

    if new_height == last_height:
        break

    last_height = new_height

# ============ END SCROLL ============

# ============ START INITIAL HERO ============
heroes = driver.find_elements(By.CSS_SELECTOR, ".mt-list-layout .mt-list-item")
heroes.reverse()

result = []
file_path  = './hero-img'
id_hero = START_FROM_ID

selected_heroes = heroes[START_FROM_ID - 1:END_ID + 1]

for hero in selected_heroes:
    name = hero.find_element(By.CSS_SELECTOR, ".mt-text span").text
    formatted_name = format_name(name)
    img_name = formatted_name + '.png'
    img = hero.find_element(By.CSS_SELECTOR, ".mt-image img")

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
    WebDriverWait(driver, 10).until(
        lambda d: img.get_attribute("src") and "data:image" not in img.get_attribute("src")
    )

    image_url = img.get_attribute("src")

    file_hero_path = f"{file_path}/{formatted_name}"

    if not os.path.exists(file_hero_path):
        os.makedirs(file_hero_path)

    download_image(image_url, file_hero_path, img_name)

    result.append(dict(
        id=id_hero,
        name=name,
        image=f"{formatted_name}/{img_name}",
    ))

    if id_hero == END_ID: break

    id_hero += 1


# ============ END INITIAL HERO ============

# ============ START DETAIL ============
for hero in result:
    hero_name = hero["name"]
    formatted_name = format_name(hero_name)
    file_skill_path  = f"./hero-img/{formatted_name}/skills"
    hero_url = f"https://www.mobilelegends.com/hero/detail?heroid={hero["id"]}"

    # Open new tab
    driver.execute_script(f"window.open('{hero_url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    wait_content = WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mt-tab-pane > div.mt-list-item > div.mt-tab-pane > div.mt-list-item"))
    )
    
    hero_detail = driver.find_element(By.CSS_SELECTOR, "div.scroll-y > div:nth-of-type(1) > div:nth-of-type(1)")
    hero_quote = hero_detail.find_element(By.CSS_SELECTOR, "div:nth-of-type(2) > div.mt-text span")
    
    hero_skill_images = driver.find_elements(By.CSS_SELECTOR, "div.mt-tab-pane > div.mt-list-item > div.mt-tabs > div.mt-list-item")

    skills = []
    for skill_element in hero_skill_images:
        skill_element.click()

        wait_skill_content = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mt-tab-pane > div.mt-list-item > div.mt-tab-pane > div.mt-list-item > div:nth-of-type(1) > div.mt-text > span"))
        )
        
        try:
            skill_image = skill_element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        except:
            skill_image = None

        hero_skill_content = driver.find_element(By.CSS_SELECTOR, "div.mt-tab-pane > div.mt-list-item > div.mt-tab-pane > div.mt-list-item")
        hero_skill_name = hero_skill_content.find_element(By.CSS_SELECTOR, "div:nth-of-type(1) > div.mt-text > span").text
        hero_skill_tags = hero_skill_content.find_elements(By.CSS_SELECTOR, "div:nth-of-type(1) > div.mt-list > .mt-list-item")

        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,"div.mt-tab-pane > div.mt-list-item > div.mt-tab-pane > div.mt-list-item > div:nth-of-type(3) > div.mt-rich-text-content"))
            )
            hero_skill_description = hero_skill_content.find_element(By.CSS_SELECTOR,"div:nth-of-type(3) > div.mt-rich-text-content")
            hero_skill_description_text = hero_skill_description.text
            hero_skill_description_html = hero_skill_description.get_attribute("innerHTML")
        except:
            hero_skill_description_text = ""
            hero_skill_description_html = ""

        tags = []
        for tag_element in hero_skill_tags:
            tag = tag_element.find_element(By.CSS_SELECTOR, "div.mt-rich-text-content")
            tags.append(tag.text)

        if not os.path.exists(file_skill_path):
            os.makedirs(file_skill_path)

        skill_image_name = None
        if skill_image:
            skill_name = hero_skill_name.lower().replace(".", "_").replace(" ", "_").replace("-", "_").replace("'", "") + '.png'
            skill_image_name = f"{formatted_name}/skills/{skill_name}"
            download_image(skill_image, file_skill_path, skill_name)

        skill = {
            "image": skill_image_name,
            "name": hero_skill_name,
            "tags": tags,
            "description_text": hero_skill_description_text,
            "description_html": hero_skill_description_html,
        }

        skills.append(skill)

    hero["skills"] = skills
    hero["quote"] = hero_quote.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# ============ END DETAIL ============

with open('heroes.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

driver.quit()