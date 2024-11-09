from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

CUI = "35722846"

options = Options()
# options.add_argument('--headless=new')
options.add_argument('--window-size=1000,1000')

driver = webdriver.Chrome(options=options)

driver.get('https://www.listafirme.ro/search.asp')
search_bar = driver.find_element(By.NAME, 'searchfor')
search_bar.click()
search_bar.send_keys(f'{CUI}\n')
sleep(0.01)

link = ""
results = driver.find_elements(By.TAG_NAME, 'a')
for r in results:
    l = r.get_attribute('href')
    if CUI in str(l):
        link = str(l)
driver.get(link)

# html = driver.page_source

driver.quit()
