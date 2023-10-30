import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class BrowserOptions(ttk.Frame):
    def __init__(self, master, controller: "MainApp", sticky, row, column):
        super().__init__(master, padding=(5, 5))
        self.controller = controller

        col = ttk.Frame(master, padding=5)
        col.grid(row=row, column=column, sticky=sticky)

        browser_options = ttk.Labelframe(col, text='Browser options', padding=(15, 10))
        browser_options.pack(side=TOP, fill=BOTH, expand=YES)

        headless = ttk.Checkbutton(browser_options, text='Show window',
                                   variable=self.controller.browser_options.get("headless"))
        headless.pack(fill=X, pady=5)
