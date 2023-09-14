import pickle
from selenium import webdriver
from conf import *
from time import sleep


options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument('--hide-scrollbars')
options.add_argument("--kiosk")
# options.add_argument('log-level=3')
driver = webdriver.Firefox(options=options)
driver.set_window_size(1280, 720)
driver.get(URL)
sleep(10)
driver.save_screenshot('./example.png')


while True:
    pass
