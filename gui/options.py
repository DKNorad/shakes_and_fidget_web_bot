import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class Options(ttk.Frame):
    def __init__(self, master, controller: "MainApp", sticky, row, column):
        super().__init__(master, padding=(5, 5))
        self.controller = controller

        col = ttk.Frame(master, padding=5)
        col.grid(row=row, column=column, rowspan=3, sticky=sticky)

        options = ttk.Labelframe(col, text='Options', padding=(15, 10))
        options.pack(side=TOP, fill=BOTH, expand=YES)

        # Tavern
        tavern1 = ttk.Checkbutton(options, text='Tavern', variable=self.controller.action_options.get("tavern"),
                                  command=lambda: tavern_cbo.configure(
                                      state=READONLY if self.controller.action_options.get("tavern").get() else DISABLED))
        tavern1.pack(fill=X, pady=5)

        tavern_cbo = ttk.Combobox(master=options, values=['Average', 'Gold', 'Experience'], state=DISABLED,
                                  textvariable=self.controller.action_sub_options.get("tavern_type"))
        tavern_cbo.current(0)
        tavern_cbo.pack(fill=X, padx=(20, 0), pady=5)

        # Arena
        arena1 = ttk.Checkbutton(options, text='Arena', variable=self.controller.action_options.get("arena"),
                                 command=lambda: arena_cbo.configure(
                                     state=READONLY if self.controller.action_options.get("arena").get() else DISABLED))
        arena1.pack(fill=X, pady=5)

        arena_cbo = ttk.Combobox(master=options, values=['Average', 'Gold', 'Experience'], state=DISABLED,
                                 textvariable=self.controller.action_sub_options.get("arena_type"))
        arena_cbo.current(0)
        arena_cbo.pack(fill=X, padx=(20, 0), pady=5)

        # Pets
        pets1 = ttk.Checkbutton(options, text='Pets', variable=self.controller.action_options.get("pets"))
        pets1.pack(fill=X, pady=5)

        # Fortress
        fort1 = ttk.Checkbutton(options, text='Fortress', variable=self.controller.action_options.get("fortress"),
                                command=lambda: [el.configure(state=NORMAL) for el in [fort2, fort3, fort4]]
                                if self.controller.action_options.get("fortress").get()
                                else [el.configure(state=DISABLED) for el in [fort2, fort3, fort4]])
        fort1.pack(fill=X, pady=5)

        fort2 = ttk.Checkbutton(master=options, text='Collect experience from the Academy', state=DISABLED,
                                variable=self.controller.action_sub_options.get("fortress_exp"))
        fort2.pack(fill=X, padx=(20, 0), pady=5)

        fort3 = ttk.Checkbutton(master=options, text='Collect stone from the Quarry', state=DISABLED,
                                variable=self.controller.action_sub_options.get("fortress_stone"))
        fort3.pack(fill=X, padx=(20, 0), pady=5)

        fort4 = ttk.Checkbutton(master=options, text='Collect wood from the Woodcutter\'s Hut', state=DISABLED,
                                variable=self.controller.action_sub_options.get("fortress_wood"))
        fort4.pack(fill=X, padx=(20, 0), pady=5)

        # Underground
        und1 = ttk.Checkbutton(options, text='Underground', variable=self.controller.action_options.get("underground"),
                               command=lambda: [el.configure(state=NORMAL) for el in [und2, und3, und4]]
                               if self.controller.action_options.get("underground").get()
                               else [el.configure(state=DISABLED) for el in [und2, und3, und4]])
        und1.pack(fill=X, pady=5)

        und2 = ttk.Checkbutton(master=options, text='Collect souls from the Soul Extractor', state=DISABLED,
                               variable=self.controller.action_sub_options.get("underground_souls"))
        und2.pack(fill=X, padx=(20, 0), pady=5)

        und3 = ttk.Checkbutton(master=options, text='Collect gold from the Gold Pit', state=DISABLED,
                               variable=self.controller.action_sub_options.get("underground_gold"))
        und3.pack(fill=X, padx=(20, 0), pady=5)

        und4 = ttk.Checkbutton(master=options, text='Lure heroes underground', state=DISABLED,
                               variable=self.controller.action_sub_options.get("underground_lure"))
        und4.pack(fill=X, padx=(20, 0), pady=5)

        # Dungeon
        dung1 = ttk.Checkbutton(options, text='Dungeon', state=DISABLED,
                                variable=self.controller.action_options.get("dungeon"))
        dung1.pack(fill=X, pady=5)

        # Abawuwu
        aba1 = ttk.Checkbutton(options, text='Dr. Abawuwu', variable=self.controller.action_options.get("abawuwu"),
                               command=lambda: [el.configure(state=NORMAL) for el in [aba2, aba3]]
                               if self.controller.action_options.get("abawuwu").get()
                               else [el.configure(state=DISABLED) for el in [aba2, aba3]])
        aba1.pack(fill=X, pady=5)

        aba2 = ttk.Checkbutton(master=options, text='Collect the daily bonus', state=DISABLED,
                               variable=self.controller.action_sub_options.get("abawuwu_daily"))
        aba2.pack(fill=X, padx=(20, 0), pady=5)

        aba3 = ttk.Checkbutton(master=options, text='Spin the wheel', state=DISABLED,
                               variable=self.controller.action_sub_options.get("abawuwu_spin"))
        aba3.pack(fill=X, padx=(20, 0), pady=5)
