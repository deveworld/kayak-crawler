import asyncio
from threading import Thread
import queue
import time
from settings import *
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

class Spider():
    def __init__(self):
        self.driver = uc.Chrome(suppress_welcome=False)#, headless=True)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = URL

    def load(self):
        self.driver.get(self.url) 

    # def loop(self):
    #     time.sleep(5)
    #     while self.power:
    #         if self.enable == False:
    #             continue
    #         loaded = 1
    #         while self.enable:
    #             log("Crawling...")
    #             if loaded % (3600/WAIT) == 0:
    #                 log("already reset")
    #                 self.already = {}
    #             Thread(target=self.check_price).start()
    #             time.sleep(WAIT)
    #             loaded += 1

    async def check_price(self):
        try:
            price = queue.Queue()
            price_thread: Thread = Thread(target=self.get_price, args=(price,))
            price_thread.start()
            while price_thread.is_alive():
                await asyncio.sleep(0.1)
        except TimeoutException:
            return (False, "Bot captcha detected")
        price = price.queue[0]
        if int(price.replace(',', '').split('원')[0]) <= MAX_PRICE:
            text = f"Found tickets below the specified price: {price}"
            return (True, text)
        else:
            text = f"Now Price: {price}"
            return (False, text)

    def get_price(self, q) -> None:
        self.load()
        try:                                                 
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[12]/div/div[3]/div/div/div/div[2]/button'))).click()
        except Exception as e:
            pass
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/main/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/div[2]/div[1]/a[1]/div[1]/div')))
        xp_prices = '/html/body/div[1]/div[1]/main/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/div[2]/div[1]/a[1]/div[1]/div/div/div[2]/span[1]'
        self.wait.until(EC.presence_of_element_located((By.XPATH,xp_prices)))
        time.sleep(15)
        q.put(self.driver.find_element(By.XPATH, xp_prices).text)