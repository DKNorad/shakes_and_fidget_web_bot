import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class Options(ttk.Frame):
    def __init__(self, master, controller: "MainApp"):
        super().__init__(master, padding=(10, 5))
        self.controller = controller

        self.pack(fill=BOTH, expand=YES, anchor=NW, side=RIGHT)

        col = ttk.Frame(self, padding=10)
        col.grid(row=0, column=0, sticky=NSEW)

        self.underground_var = IntVar(col, 0)

        options = ttk.Labelframe(col, text='Options', padding=(15, 10))
        options.pack(side=TOP, fill=BOTH, expand=YES)

        # Tavern
        tavern1 = ttk.Checkbutton(options, text='Tavern')
        tavern1.pack(fill=X, pady=5)

        cbo = ttk.Combobox(master=options, values=['Average', 'Gold', 'Experience'], state=READONLY)
        cbo.current(0)
        cbo.pack(fill=X, padx=(20, 0), pady=5)

        # Arena
        arena1 = ttk.Checkbutton(options, text='Arena')
        arena1.pack(fill=X, pady=5)

        cbo = ttk.Combobox(master=options, values=['Average', 'Gold', 'Experience'], state=READONLY)
        cbo.current(0)
        cbo.pack(fill=X, padx=(20, 0), pady=5)

        # Pets
        pets1 = ttk.Checkbutton(options, text='Pets')
        pets1.pack(fill=X, pady=5)

        # Fortress
        fortress1 = ttk.Checkbutton(options, text='Fortress')
        fortress1.pack(fill=X, pady=5)

        fortress2 = ttk.Checkbutton(master=options, text='Collect experience from the Academy')
        fortress2.pack(fill=X, padx=(20, 0), pady=5)

        fortress3 = ttk.Checkbutton(master=options, text='Collect stone from the Quarry')
        fortress3.pack(fill=X, padx=(20, 0), pady=5)

        fortress4 = ttk.Checkbutton(master=options, text='Collect wood from the Woodcutter\'s Hut')
        fortress4.pack(fill=X, padx=(20, 0), pady=5)

        # Underground
        underground1 = ttk.Checkbutton(options, text='Underground', variable=self.underground_var)
        underground1.pack(fill=X, pady=5)

        underground2 = ttk.Checkbutton(master=options, text='Collect souls from the Soul Extractor')
        underground2.pack(fill=X, padx=(20, 0), pady=5)

        underground3 = ttk.Checkbutton(master=options, text='Collect gold from the Gold Pit')
        underground3.pack(fill=X, padx=(20, 0), pady=5)

        underground4 = ttk.Checkbutton(master=options, text='Lure heroes underground')
        underground4.pack(fill=X, padx=(20, 0), pady=5)

        # Dungeon
        underground1 = ttk.Checkbutton(options, text='Dungeon', state=DISABLED)
        underground1.pack(fill=X, pady=5)
