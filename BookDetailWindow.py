from dataclasses import dataclass
from tkinter import N, E, S, W, Toplevel, ttk, StringVar
from tkinter.ttk import Frame
from typing import Dict, Any, Callable


@dataclass
class BookDetails:
    ISBN: int
    title: str
    author: str
    publisher: str
    category: str
    price: float
    new_quantity: int = 0
    old_quantity: int = 0

    def total_quantity(self) -> int:
        return self.new_quantity + self.old_quantity


class BookDetailWindow:

    def __init__(self, root: Toplevel, book_info: BookDetails, ok_callback: Callable[[BookDetails], None]):
        self.root = root
        self.book_info = book_info
        self.ok_callback = ok_callback

        self.root.title("Book Info for " + str(book_info.ISBN))
        self.root.maxsize(1000, 1000)
        self.root.minsize(500, 600)

        mainframe = Frame(self.root, padding="3 3 12 12")
        mainframe.grid(row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Title").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Author").grid(column=0, row=1, sticky=W)
        self.author_var = StringVar(value=book_info.author)
        self.author_entry = ttk.Entry(mainframe, width=20, textvariable=self.author_var)
        self.author_entry.grid(column=1, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Publisher").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Category").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Price").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="New Quantity").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Total Quantity").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, width=20, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))


