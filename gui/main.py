import ttkbootstrap as ttk
from gui.credentials_entry import CredentialsEntry
from gui.options import Options
from webdriver import WebDriver


class MainApp:
    def __init__(self):
        self.app = ttk.Window("Shakes & Fidget Bot", "superhero", resizable=(False, False))

        self.username = ttk.StringVar(value="")
        self.password = ttk.StringVar(value="")
        self.url = ttk.StringVar(value="https://sfgame.net/")
        self.options = {
            "username": 123
        }

        self.driver = WebDriver(self)
        CredentialsEntry(self.app, self)
        Options(self.app, self)

    def run(self):
        self.app.mainloop()

    def start_webdriver(self):
        self.driver.run()

    def stop_webdriver(self):
        self.driver.stop()
