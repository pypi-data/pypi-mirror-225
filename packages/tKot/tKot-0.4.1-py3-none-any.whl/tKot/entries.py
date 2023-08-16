import tkinter as tk
from typing import Callable


class TopEntry:
    def __init__(self,
                 master: tk.TOP,
                 w: int, h: int,
                 x: int, y: int,
                 desc: list[str],
                 value: str,
                 callback: Callable[[list[str], str], bool]):
        self.top = tk.Toplevel(master)
        self.top.overrideredirect(True)
        self.top.bind("<FocusOut>", lambda e: self.top.destroy())
        self.top.geometry(F"{w}x{h}+{x}+{y}")
        self.desc = desc
        """descriptor"""
        self.variable = tk.StringVar(
            master=self.top,
            value=value)
        self.entry = tk.Entry(
            master=self.top,
            textvariable=self.variable,
            )
        self.entry.bind("<Return>", self.__set_value)
        self.entry.bind("<Escape>", lambda e: self.top.destroy())
        self.entry.pack()
        self.cb = callback
        self.top.lift(master)
        self.entry.focus_set()

    def __set_value(self, e: tk.Event):
        try:
            self.cb(self.desc, self.variable.get())
            self.top.destroy()
        except ValueError as e:
            self.entry.configure(background="red")
