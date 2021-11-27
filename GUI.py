import math
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox
from googleapiclient.discovery import build

import pandas as pd
from pandastable import Table


def on_closing():
    mainWindow.destroy()
    exit()


def reformat_name(raw_name: str) -> str:
    """
    Reformats a name from "first (middle) last" to "last, first"
    input: name
    output: name in "Last, first (middle)" format
    """
    author_names = raw_name.split(" ", maxsplit=1)
    if len(author_names) > 1:
        return author_names[1] + ", " + author_names[0]
    else:
        return raw_name


class KafnaGUI(Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        with open("key.txt", "r") as f:
            api_key = f.readline().strip()
        service = build("books", "v1", developerKey=api_key)
        self.volumes = service.volumes()

        self.master = master
        self.master.title("Kafna")
        self.master.maxsize(1000, 600)
        self.master.minsize(1000, 600)

        c = Canvas(self.master)
        c.configure(yscrollincrement='10c')

        # create all of the main containers
        mainframe = Frame(self.master, pady=3)
        mainframe.grid(row=0, sticky=(N, W, E, S))

        # layout all of the main containers
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create container for table
        self.center = Frame(self.master, bg='gray2', pady=3)
        self.center.grid(row=1, sticky="nsew")

        # create the widgets for the top frame
        self.isbn = StringVar()
        self.isbn_entry = Entry(mainframe, width=50, textvariable=self.isbn)
        self.category = StringVar()
        self.category_combobox = Combobox(mainframe, textvariable=self.category)
        self.saveButton = tkinter.Button(mainframe, text="Save", command=self.save)

        # layout the widgets in the top frame
        self.isbn_entry.grid(row=0, column=0, sticky=(W, E))
        self.category_combobox.grid(row=0, column=1, sticky=(W, E))
        self.saveButton.grid(row=0, column=2, sticky=(E, ))

        # Configure widgets and bind callbacks
        self.category_combobox["values"] = ("", "@", "Ableism", "Abuse", "Africa")
        self.category_combobox.state(["readonly"])
        self.isbn_entry.bind("<Return>", self.isbn_changed)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.fileName = askopenfilename()  # show an open file dialog box and return the path to the selected file
        if self.fileName:
            self.data = pd.read_excel(self.fileName)
        else:
            self.data = pd.DataFrame(columns=["Item Name", "Description", "Category",
                                              "SKU", "Variation Name", "Price", "Current Quantity Groundwork Books",
                                              "New Quantity Groundwork Books", "Stock Alert Enabled Groundwork Books",
                                              "Stock Alert Count Groundwork Books", "Tax - Sales Tax (7.75%)"])
            self.fileName = "book_log.xlsx"
        self.ISBN_quantity_dict = dict(zip(self.data["SKU"], self.data["New Quantity Groundwork Books"] + self.data[
            "Current Quantity Groundwork Books"].fillna(0)))

        self.newBooks = pd.DataFrame(columns=self.data.columns)

        self.bookTable = Table(self.center, dataframe=self.newBooks, showtoolbar=False, showstatusbar=True, height=450)
        self.bookTable.adjustColumnWidths(30)
        self.bookTable.show()
        self.bookTable.redraw()

    def save(self):
        print("Writing to file...")
        self.data.to_excel(self.fileName, index=False)
        print("Done writing")

    def isbn_changed(self, *args):
        self.web_log(self.isbn.get(), self.category_combobox.get())

    def web_log(self, ISBN, category):
        output = self.volumes.list(q="isbn:" + ISBN, maxResults=1).execute()
        if "items" not in output or len(output["items"]) == 0:
            print("No book found with this ISBN.")
            info = {}
        else:
            info = output["items"][0]["volumeInfo"]

        # handle the case where the input is ISBN 10, not 13. We convert it to
        # ISBN 13 if possible. Else, send warning.
        if ISBN[:3] != "978" and ISBN[:3] != "979":
            found13 = False
            if "industryIdentifiers" in info:
                for identifier in info["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_13":
                        found13 = True
                        ISBN = identifier["identifier"]
            if not found13:
                print("The ISBN number you typed in is ISBN 10, not ISBN13. There is no ISBN13 number in the database for this book.")
                ISBN_in = input("Enter ISBN 13 manually: ").strip()
                if ISBN_in:
                    ISBN = ISBN_in

        quantity, in_log = self.merge_book(ISBN)
        if in_log:
            print("Already in inventory, new quantity increased from {} to {}".format(self.ISBN_quantity_dict[int(ISBN)] - 1,
                                                                                      self.ISBN_quantity_dict[int(ISBN)]))
        else:
            # get the information we need
            if "authors" in info and len(info["authors"]) > 0:
                author = info["authors"][0]
                print("Author: " + author)
            else:
                author = input("Author info is not available, enter manually (firstname lastname): ").strip()

            if "publisher" in info:
                publisher = info['publisher']
                print("Publisher: " + publisher)
            else:
                publisher = input("Publisher info is not available, enter manually: ").strip()

            if "title" in info:
                title = info['title']
                if "subtitle" in info:
                    # if the book has a subtitle, use the subtitle as well.
                    subtitle = info['subtitle']
                    title = title + ": " + subtitle
                print("Title: " + title)
            else:
                title = input("Title info is not available, enter manually: ").strip()

            author = reformat_name(author)
            price = input("Enter the price of this book: ")
            self.ISBN_quantity_dict[int(ISBN)] = 1
            self.data = self.data.append({"Item Name": title, "Description": publisher, "Category": category, "SKU": int(ISBN),
                                          "Variation Name": author, "Price": float(price),
                                          "Current Quantity Groundwork Books": "",
                                          "New Quantity Groundwork Books": 1, "Stock Alert Enabled Groundwork Books": "",
                                          "Stock Alert Count Groundwork Books": "", "Tax - Sales Tax (7.75%)": "Y"},
                                         ignore_index=True)


    def merge_book(self, ISBN):
        in_log = False
        quantity = 1

        # check if book is in book_log.xlsx
        ISBN = int(ISBN)
        if ISBN in self.ISBN_quantity_dict:
            if math.isnan(self.data.loc[self.data["SKU"] == ISBN, "New Quantity Groundwork Books"]):
                self.data.loc[self.data["SKU"] == ISBN, "New Quantity Groundwork Books"] = 0
                self.ISBN_quantity_dict[ISBN] = 0
            self.ISBN_quantity_dict[ISBN] += 1
            in_log = True

            self.data.loc[self.data["SKU"] == ISBN, "New Quantity Groundwork Books"] += 1
            quantity = self.data.loc[self.data["SKU"] == ISBN, "New Quantity Groundwork Books"]

        return quantity, in_log


if __name__ == '__main__':
    mainWindow = tkinter.Tk()
    lightPanelGUIInstance = KafnaGUI(mainWindow)
    mainWindow.protocol("WM_DELETE_WINDOW", on_closing)
    mainWindow.mainloop()