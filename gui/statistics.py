import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import MainApp


class Statistics(ttk.Frame):
    def __init__(self, master, controller: "MainApp", sticky, row, column):
        super().__init__(master, padding=(5, 5))
        self.controller = controller

        col = ttk.Frame(master, padding=5)
        col.grid(row=row, column=column, sticky=sticky)

        # Statistics frame
        statistics = ttk.Labelframe(col, text='Statistics', padding=(15, 10))
        statistics.pack(side=TOP, fill=BOTH, expand=YES)

        sessions = ttk.Label(statistics, text=f'Sessions: {self.controller.statistics["sessions"]}')
        sessions.pack(fill=X, pady=5)

        # Tavern statistics
        arena = ttk.Label(statistics, text='Tavern:')
        arena.pack(fill=X, pady=(5, 0))
        arena_stats = ttk.Label(statistics,
                                text=f'Gold: {self.controller.statistics["tavern_gold"]}\n'
                                     f'Experience: {self.controller.statistics["tavern_exp"]}')
        arena_stats.pack(fill=X, pady=(0, 5))

        # Arena statistics
        arena = ttk.Label(statistics, text='Arena:')
        arena.pack(fill=X, pady=(5, 0))
        arena_stats = ttk.Label(statistics,
                                text=f'Attacks: {self.controller.statistics["arena_attacks"]}\n'
                                     f'W/L ratio: {round(self.controller.statistics["arena_wins"] / self.controller.statistics["arena_attacks"] * 100, 2)} %')
        arena_stats.pack(fill=X, pady=(0, 5))
