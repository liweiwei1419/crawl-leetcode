import requests
from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number/description/"
executable_path = "C:\\Users\\Administrator\\Desktop\\crawl-leetcode\\geckodriver-v0.19.1-win64\\geckodriver.exe"

# driver = webdriver.Firefox(executable_path=executable_path)
driver = webdriver.PhantomJS(executable_path="C:\\Users\\Administrator\\Desktop\\crawl-leetcode\\phantomjs.exe")
driver.get(url)
html = driver.page_source

# response =requests.get(url)
# html = response.text
soup = BeautifulSoup(html, 'lxml')

question_description = soup.select(
    "#descriptionContent > div.col-md-9.question-panel > div > div.question-description__3U1T")
driver.close()
print(question_description[0])
print('end')
