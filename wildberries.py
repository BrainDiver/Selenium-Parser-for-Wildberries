from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from time import sleep
from fake_useragent import UserAgent

proxy_query=input("Enter proxy if they need, example IP:PORT ")
query=input("Enter search query ")
print("Okey lets go")
useragent=UserAgent()
options=Options()
options.add_argument(f"user-agent={useragent.random}")
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

#Program look need proxy or not
if len(proxy_query)>1:
    options.add_argument(f"--proxy-server={proxy_query}")
else:
    pass

serv=Service("./chromedriver")
url="https://wildberries.ru"
driver=webdriver.Chrome(service=serv, options=options)
products=[]

@dataclass
class Product_item:
    title:str
    link:str
    price:str
    def to_dict(self):
        return {"title": self.title, "price": self.price, "link": self.link}

try:
    driver.get(url)
    print("Site opened")
    first_sleep= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div/div[3]/div[1]/div/ul[1]/li[1]/div/div/a/div/img')))
    print("Start search")
    search=driver.find_element(By.ID, "searchInput")
    search.clear()
    search.send_keys(query)
    search.send_keys(Keys.ENTER)
    second_sleep= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/button')))
    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div/div/div[3]/div/div/div/div/div[1]/div[2]/button').click()
    sleep(0.5)
    driver.find_element(By.XPATH, '//span[text()="По новинкам"]').click()
    sleep(0.5)
    last_height=driver.find_element(By.CLASS_NAME, "wrapper").get_attribute("scrollHeight")
    print("Start scroling page")
    while True:
        driver.execute_script(f"window.scrollTo(0, {last_height}-1500)")
        sleep(1)
        new_height=driver.find_element(By.CLASS_NAME, "wrapper").get_attribute("scrollHeight")
        if last_height==new_height:
            print("Finished")
            break
        last_height=new_height
        print("Collect products")
    elements=driver.find_elements(By.CLASS_NAME, "product-card__main.j-card-link")
    elements=elements
    for element in elements:
        element_link=element.get_attribute("href")
        element_price=element.find_element(By.CLASS_NAME, "price__lower-price").text
        element_title=element.find_element(By.CLASS_NAME, "goods-name").text[2:]
        element_result=Product_item(title=element_title, link=element_link, price=element_price )
        products.append(element_result.to_dict())
        print(f' title: {products[elements.index(element)].get("title")}', "\n", f'price: {products[elements.index(element)].get("price")}', "\n", f'link: {products[elements.index(element)].get("link")}')
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
