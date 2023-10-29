from pathlib import Path
from selenium.webdriver import Firefox, FirefoxOptions
from actions.actions import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class WebDriver:
    def __init__(self, controller: "MainApp"):
        self.controller = controller

        if not Path(Path.cwd().joinpath("../ff_selenium_profile")).is_dir():
            Path.cwd().joinpath("../ff_selenium_profile").mkdir()

        self.options = FirefoxOptions()
        self.options.add_argument("--kiosk")
        self.options.add_argument('-profile')
        self.options.add_argument(Path.cwd().joinpath("../ff_selenium_profile").as_posix())
        self.driver = None
        self.action = None

    def run(self):
        if not self.driver:
            if not self.controller.browser_options.get("headless").get():
                self.options.add_argument('--headless')

            self.driver = Firefox(self.options)
            self.driver.set_window_size(1280, 720)

            self.action = Action(self.driver, self.controller)
            self.driver.get(self.controller.url.get())
            self.controller.print_output("The browser has been started.")
        else:
            self.controller.print_output("The browser is already running.")

    def stop(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.action = None
            self.controller.print_output("The browser has been closed.")
        else:
            self.controller.print_output("The browser is not running.")
