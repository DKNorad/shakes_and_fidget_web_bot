from datetime import datetime
from pathlib import Path
from tkinter import Text
import ttkbootstrap as ttk

from gui.browser_options import BrowserOptions
from gui.credentials_entry import CredentialsEntry
from gui.options import Options
from gui.output import Output
from gui.statistics import Statistics
from webdriver.webdriver import WebDriver


class MainApp:
    def __init__(self):
        self.app = ttk.Window("Shakes & Fidget Bot", "superhero", resizable=(False, False),
                              iconphoto=str(Path.cwd().joinpath('gui/assets/icon.png')))

        self.username = ttk.StringVar(value="")
        self.password = ttk.StringVar(value="")
        self.url = ttk.StringVar(value="https://sfgame.net/")
        self.options = {
            "tavern": ttk.IntVar(),
            "tavern_type": ttk.StringVar(),
            "arena": ttk.IntVar(),
            "arena_type": ttk.StringVar(),
            "pets": ttk.IntVar(),
            "fortress": ttk.IntVar(),
            "fortress_exp": ttk.IntVar(value=1),
            "fortress_stone": ttk.IntVar(value=1),
            "fortress_wood": ttk.IntVar(value=1),
            "underground": ttk.IntVar(),
            "underground_souls": ttk.IntVar(value=1),
            "underground_gold": ttk.IntVar(value=1),
            "underground_lure": ttk.IntVar(value=1),
            "dungeon": ttk.IntVar(),
            "abawuwu": ttk.IntVar(),
            "abawuwu_daily": ttk.IntVar(value=1),
            "abawuwu_spin": ttk.IntVar(value=1),
        }
        self.browser_options = {
            "headless": ttk.IntVar()
        }

        self.statistics = {
            "sessions": 11,
            "tavern_gold": 125789,
            "tavern_exp": 12587,
            "arena_attacks": 77,
            "arena_wins": 13
        }

        self.driver = WebDriver(self)

        # Using the ScrolledText widget from ttkbootstrap but have Text as a type hint as the functions are missing.
        self.output_box: Text = None

        CredentialsEntry(self.app, self, "NEWS", 0, 0)
        BrowserOptions(self.app, self, "NEWS", 1, 0)
        Statistics(self.app, self, "NEWS", 2, 0)
        Options(self.app, self, "NW", 0, 1)
        Output(self.app, self, "NW", 0, 2)

    def print_output(self, text):
        # Accessing the _text protected method to configure the Text widget state which is used for ScrolledText.
        self.output_box._text.configure(state='normal')
        self.output_box.insert('end', f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: {text}\n')
        self.output_box.see('end')
        self.output_box._text.configure(state='disabled')

    def run(self):
        self.app.mainloop()

    def start_webdriver(self):
        if not self.username.get():
            self.print_output("The username field is empty.")
        elif not self.password.get():
            self.print_output("The password field is empty.")
        else:
            self.driver.run()
            self.perform_actions()

    def stop_webdriver(self):
        self.driver.stop()

    def perform_actions(self):
        action = self.driver.action
        actions = {
            "tavern": action.tavern,
            "arena": action.arena,
            "pets": action.pets,
            "fortress": action.fortress,
            "underground": action.underground,
            "dungeon": action.dungeons,
        }

        action.login()
        for option in self.options.items():
            if option[1].get() == 1:
                actions[option[0]]()
