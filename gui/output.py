import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from tkinter import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class Output(ttk.Frame):
    def __init__(self, master, controller: "MainApp"):
        super().__init__(master, padding=(5, 5))
        self.controller = controller

        self.pack(fill=BOTH, expand=YES, anchor=NW, side=RIGHT)

        col = ttk.Frame(self, padding=5)
        col.grid(row=0, column=3, sticky=NSEW)

        output = ttk.Labelframe(col, text='Output', padding=(5, 0))
        output.pack(side=TOP, fill=BOTH, expand=YES)

        # Output
        self.controller.output_box = ScrolledText(output, padding=5, height=20, width=80,
                                                  autohide=True, state='disabled')
        self.controller.output_box.pack(fill=X, pady=5)
