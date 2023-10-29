from datetime import datetime
from pathlib import Path
from tkinter import Text
from ttkbootstrap.scrolled import ScrolledText
import ttkbootstrap as ttk
from gui.credentials_entry import CredentialsEntry
from gui.options import Options
from gui.output import Output
from webdriver import WebDriver


class MainApp:
    def __init__(self):
        self.app = ttk.Window("Shakes & Fidget Bot", "superhero", resizable=(False, False),
                              iconphoto=str(Path.cwd().joinpath('gui/assets/icon.png')))

        self.username = ttk.StringVar(value=None)
        self.password = ttk.StringVar(value=None)
        self.url = ttk.StringVar(value="https://sfgame.net/")
        self.options = {
            "tavern": ttk.IntVar(),
            "tavern_type": ttk.StringVar(),
            "arena": ttk.IntVar(),
            "arena_type": ttk.StringVar(),
            "pets": ttk.IntVar(),
            "fortress": ttk.IntVar(),
            "fortress_exp": ttk.IntVar(),
            "fortress_stone": ttk.IntVar(),
            "fortress_wood": ttk.IntVar(),
            "underground": ttk.IntVar(),
            "underground_souls": ttk.IntVar(),
            "underground_gold": ttk.IntVar(),
            "underground_lure": ttk.IntVar(),
            "dungeon": ttk.IntVar(),
        }
        self.browser_options = {
            "headless": ttk.IntVar()
        }

        self.driver = WebDriver(self)

        self.output_box: Text = ScrolledText()

        CredentialsEntry(self.app, self)
        Options(self.app, self)
        Output(self.app, self)

    def print_output(self, text):
        self.output_box.insert('end', f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: {text}\n')
        self.output_box.see('end')

    def run(self):
        self.app.mainloop()

    def start_webdriver(self):
        if not self.username.get():
            self.print_output("The username field is empty.")
        elif not self.password.get():
            self.print_output("The password field is empty.")
        else:
            self.driver.run()

    def stop_webdriver(self):
        self.driver.stop()

