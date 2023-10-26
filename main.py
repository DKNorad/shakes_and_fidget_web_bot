import sys
from actions import Action
from selenium.webdriver import Firefox, FirefoxOptions
from conf import URL
from time import sleep
from pathlib import Path


if not Path(Path.cwd().joinpath("ff_selenium_profile")).is_dir():
    Path.cwd().joinpath("ff_selenium_profile").mkdir()

options = FirefoxOptions()
# options.add_argument('--headless')
options.add_argument("--kiosk")
options.add_argument('-profile')
options.add_argument(Path.cwd().joinpath("ff_selenium_profile").as_posix())
driver = Firefox(options)
driver.set_window_size(1280, 720)
action = Action(driver)

driver.get(URL)

try:
    while True:
        if action.login():
            break

    while True:
        action.abawuwu()
        action.tavern()
        action.arena()
        action.pets()
        action.fortress()
        sleep(200000)

except KeyboardInterrupt:
    print("Interrupt")
    driver.quit()
except Exception as e:
    print(e)
    driver.quit()

