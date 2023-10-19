from actions import Action
from selenium.webdriver import Firefox, FirefoxOptions
from conf import URL
from time import sleep
from pathlib import Path

try:
    if not Path(Path.cwd().joinpath("ff_selenium_profile")).is_dir():
        Path.cwd().joinpath("ff_selenium_profile").mkdir()

    options = FirefoxOptions()
    # options.add_argument('--headless')
    options.add_argument("--kiosk")
    options.add_argument('-profile')
    options.add_argument(Path.cwd().joinpath("ff_selenium_profile").as_posix())
    driver = Firefox(options)
    driver.set_window_size(1280, 720)
    driver.get(URL)
    action = Action(driver)

    while True:
        if action.login():
            break

    while True:
        action.abawuwu()
        action.arena()
        action.pets()
        action.tavern()
        sleep(200000)

except:
    driver.quit()
    quit()
