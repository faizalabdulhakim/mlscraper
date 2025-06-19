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

id_hero = 71

driver.get(f"https://www.mobilelegends.com/hero/detail?heroid={id_hero}")

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

    # wait_description = WebDriverWait(driver, 5).until(
    #     EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.mt-tab-pane > div.mt-list-item > div.mt-tab-pane > div.mt-list-item > div:nth-of-type(3) > div.mt-rich-text-content"))
    # )

    # hero_skill_description = hero_skill_content.find_element(By.CSS_SELECTOR, "div:nth-of-type(3) > div.mt-rich-text-content")
    # hero_skill_description_text = hero_skill_description.text
    # hero_skill_description_html = hero_skill_description.get_attribute("innerHTML")

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

    skill = {
        "image": skill_image,
        "name": hero_skill_name,
        "tags": tags,
        "description_text": hero_skill_description_text,
        "description_html": hero_skill_description_html,
    }

    skills.append(skill)

print(json.dumps(skills, ensure_ascii=False, indent=2))