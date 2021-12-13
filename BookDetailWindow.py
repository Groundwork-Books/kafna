import re
import tkinter
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
    new_quantity: int = 1
    old_quantity: int = 0

    def total_quantity(self) -> int:
        return self.new_quantity + self.old_quantity


def check_int(str_val):
    return re.match(r'^[0-9]*$', str_val) is not None


def check_price(str_val):
    return re.match(r'^[0-9]*\.?[0-9]{,2}$', str_val) is not None


class BookDetailWindow:

    def __init__(self, root: Toplevel, book_info: BookDetails, ok_callback: Callable[[BookDetails], None]):
        self.root = root
        self.book_info = book_info
        self.ok_callback = ok_callback

        self.root.title("Book Info for " + str(book_info.ISBN))
        self.root.maxsize(1000, 1000)
        self.root.minsize(500, 600)

        check_int_wrapper = (root.register(check_int), '%P')
        check_price_wrapper = (root.register(check_price), '%P')

        mainframe = Frame(self.root, padding="3 3 12 12")
        mainframe.grid(row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Title").grid(column=0, row=0, sticky=W)
        self.title_var = StringVar(value=book_info.title)
        self.title_entry = ttk.Entry(mainframe, textvariable=self.title_var)
        self.title_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Label(mainframe, text="Author").grid(column=0, row=1, sticky=W)
        self.author_var = StringVar(value=book_info.author)
        self.author_entry = ttk.Entry(mainframe, textvariable=self.author_var)
        self.author_entry.grid(column=1, row=1, sticky=(W, E))

        ttk.Label(mainframe, text="Publisher").grid(column=0, row=2, sticky=W)
        self.publisher_var = StringVar(value=book_info.publisher)
        self.publisher_entry = ttk.Entry(mainframe, textvariable=self.publisher_var)
        self.publisher_entry.grid(column=1, row=2, sticky=(W, E))

        ttk.Label(mainframe, text="Category").grid(column=0, row=3, sticky=W)
        self.category_var = StringVar(value=book_info.category)
        self.category_entry = ttk.Entry(mainframe, textvariable=self.category_var)
        self.category_entry.grid(column=1, row=3, sticky=(W, E))

        ttk.Label(mainframe, text="Price").grid(column=0, row=4, sticky=W)
        self.price_var = StringVar(value=str(book_info.price))
        self.price_entry = ttk.Entry(mainframe, textvariable=self.price_var, validate="key",
                                     validatecommand=check_price_wrapper)
        self.price_entry.grid(column=1, row=4, sticky=(W, E))

        ttk.Label(mainframe, text="New Quantity").grid(column=0, row=5, sticky=W)
        self.new_quantity_var = StringVar(value=str(book_info.new_quantity))
        self.new_quantity_entry = ttk.Entry(mainframe, textvariable=self.new_quantity_var, validate="key",
                                            validatecommand=check_int_wrapper)
        self.new_quantity_entry.grid(column=1, row=5, sticky=(W, E))

        ttk.Label(mainframe, text="Total Quantity").grid(column=0, row=6, sticky=W)
        self.total_quantity_var = StringVar(value=str(book_info.total_quantity()))
        self.total_quantity_label = ttk.Label(mainframe, textvariable=self.total_quantity_var)
        self.total_quantity_label.grid(column=1, row=6, sticky=(W, E))

        self.cancel_button = ttk.Button(mainframe, text="Cancel", command=self.cancel)
        self.cancel_button.grid(column=0, row=7, sticky=(W,E))

        self.submit_button = ttk.Button(mainframe, text="Save", command=self.submit)
        self.submit_button.grid(column=1, row=7, sticky=(W,E))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.new_quantity_var.trace_add("write", self.update_total_quantity)

        if book_info.old_quantity != 0:
            self.title_entry.state(['readonly'])
            self.author_entry.state(['readonly'])
            self.publisher_entry.state(['readonly'])
            self.category_entry.state(['readonly'])
            self.price_entry.state(['readonly'])

    def update_total_quantity(self, *args):
        if self.new_quantity_var.get() == "":
            self.total_quantity_var.set(str(self.book_info.old_quantity))
        else:
            self.total_quantity_var.set(str(self.book_info.old_quantity + int(self.new_quantity_var.get())))

    def cancel(self):
        self.root.destroy()

    def submit(self, *args):
        self.book_info.title = self.title_var.get()
        self.book_info.author = self.author_var.get()
        self.book_info.publisher = self.publisher_var.get()
        self.book_info.category = self.category_var.get()
        if self.price_var.get() == "":
            self.price_var.set("0")
        self.book_info.price = float(self.price_var.get())
        if self.new_quantity_var.get() == "":
            self.new_quantity_var.set("0")
        self.book_info.new_quantity = int(self.new_quantity_var.get())
        self.ok_callback(self.book_info)
        self.root.destroy()


if __name__ == '__main__':
    mainWindow = tkinter.Tk()
    lightPanelGUIInstance = BookDetailWindow(mainWindow, BookDetails(978000000, "CManifesto", "Marx", "PM", "MARX", 4), print)
    # mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
    mainWindow.mainloop()