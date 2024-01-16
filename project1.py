from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# 크롬을 열어줍니다
driver = webdriver.Chrome()
driver.maximize_window()

# 해당 사이트를 열어서 데이터 크롤링을 준비합니다
project_search_url = "https://www.inflearn.com/courses"
driver.get(project_search_url)

ind = 1
list1 = []

for i in range(24):
    title = driver.find_element(by = 'xpath', value = f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i+1}]/div/a/div[2]/div[1]').text
    price = driver.find_element(by = 'xpath', value = f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i+1}]/div/a/div[2]/div[4]').text
    element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="courses_section"]/div/div/div/main/div[4]/div/div[{i+1}]/div/a/div[1]/figure/img')))
    driver.execute_script("arguments[0].click();", element)
    grade = driver.find_element(by = 'xpath', value = f'//*[@id="main"]/section/div[1]/div[1]/div/div/div[2]/div[3]/span[1]/strong').text
    students = driver.find_element(by = 'xpath', value = f'//*[@id="main"]/section/div[1]/div[1]/div/div/div[2]/div[3]/span[2]/strong').text
    difficulty = driver.find_element(by = 'xpath', value = f'//*[@id="description"]/h2[1]/strong[1]').text
    time1 = driver.find_element(by = 'xpath', value = f'//*[@id="main"]/section/div[1]/div[2]/div[2]/div/div[2]').text
    driver.back()
    list1.append([title,grade, price, difficulty, price, time1])
    time.sleep(3)

# click 이 안먹는 이유를 생각
## 로딩 시간이 충분히 일어날 수 있도록 확인하기
## 에러가 일어난 곳을 따로 확인하기

print(list1)