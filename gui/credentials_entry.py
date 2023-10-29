import threading

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class CredentialsEntry(ttk.Frame):
    def __init__(self, master, controller: "MainApp"):
        super().__init__(master, padding=(5, 5))
        self.controller = controller

        self.pack(fill=BOTH, expand=YES, anchor=NW, side=LEFT)

        col = ttk.Frame(self, padding=5)
        col.grid(row=0, column=0, sticky=NSEW)

        # Login frame
        login = ttk.Labelframe(col, text='Login', padding=(15, 10))
        login.pack(side=TOP, fill=BOTH, expand=YES)

        first_row = ttk.Frame(login)
        first_row.pack(fill=X, expand=YES)
        ttk.Label(first_row, text="Username:", width=10).pack(fill=X, padx=5, side=LEFT)
        ttk.Entry(first_row, textvariable=self.controller.username).pack(fill=X, padx=5, pady=5, side=LEFT, expand=YES)

        second_row = ttk.Frame(login)
        second_row.pack(fill=X, expand=YES)
        ttk.Label(second_row, text="Password:", width=10).pack(fill=X, padx=5, side=LEFT)
        ttk.Entry(second_row, textvariable=self.controller.password, show="*").pack(fill=X, padx=5, pady=5,
                                                                                           side=LEFT, expand=YES)

        third_row = ttk.Frame(login)
        third_row.pack(fill=X, expand=YES)
        ttk.Label(third_row, text="Url", width=10).pack(fill=X, padx=5, side=LEFT)
        ttk.Entry(third_row, textvariable=self.controller.url).pack(fill=X, padx=5, pady=5, side=LEFT, expand=YES)

        fourth_row = ttk.Frame(login)
        fourth_row.pack(fill=X, expand=YES, pady=(5, 0))
        ttk.Button(fourth_row, text="Start",
                   command=lambda: threading.Thread(target=self.controller.start_webdriver).start(),
                   bootstyle=SUCCESS, width=6).pack(side=RIGHT, padx=5)

        ttk.Button(fourth_row, text="Stop",
                   command=lambda: threading.Thread(target=self.controller.stop_webdriver).start(),
                   bootstyle=DANGER, width=6).pack(side=RIGHT, padx=5)

        # Browser options.
        browser_options = ttk.Labelframe(col, text='Browser options', padding=(15, 10))
        browser_options.pack(side=TOP, fill=BOTH, expand=YES)

        headless = ttk.Checkbutton(browser_options, text='Show window',
                                   variable=self.controller.browser_options.get("headless"))
        headless.pack(fill=X, pady=5)
