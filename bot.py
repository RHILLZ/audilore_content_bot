import os
import subprocess
import random
from unicodedata import name

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Bot:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        self.service = Service('/Users/rhillx/Downloads/chromedriver')
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        

    def findClip(self, topics):
        topic = random.choice(topics)
        self.driver.get("https://search.audioburst.com")
        secs = self.driver.find_elements(By.CLASS_NAME,'h2')
        print(secs)
        
b = Bot()
b.findClip(['Business', 'Tech'])
