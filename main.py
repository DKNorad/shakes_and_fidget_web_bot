from actions import Action
import pickle
from selenium import webdriver
from conf import URL
from time import sleep


options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
options.add_argument("--kiosk")

driver = webdriver.Firefox(options)
driver.set_window_size(1280, 720)
driver.get(URL)
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
except FileNotFoundError:
    pass
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

action = Action(driver)

while True:
    if action.login():
        break

while True:
    action.arena()
    action.pets()
    sleep(20)
