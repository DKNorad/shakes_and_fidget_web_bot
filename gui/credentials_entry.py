import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class CredentialsEntry(ttk.Frame):
    def __init__(self, master, controller: "MainApp"):
        super().__init__(master, padding=(10, 5))
        self.controller = controller

        self.pack(fill='none', expand=YES, side=LEFT, anchor=NW)

        # form entries
        self.create_form_entry("username", self.controller.username)
        self.create_form_entry("password", self.controller.password, show_chr="*")
        self.create_form_entry("url", self.controller.url)
        self.create_buttonbox()

    def create_form_entry(self, label, variable, show_chr=""):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable, show=show_chr)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        """Create the application buttonbox"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttk.Button(master=container, text="Start", command=self.controller.start_webdriver, bootstyle=SUCCESS, width=6)
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttk.Button(master=container, text="Stop", command=self.controller.stop_webdriver, bootstyle=DANGER, width=6)
        cnl_btn.pack(side=RIGHT, padx=5)

