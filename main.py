import math

from googleapiclient.discovery import build
import os

import pandas as pd

# the documentation of the API can be found here: https://openlibrary.org/dev/docs/api/books


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


def update_books():
    global ISBN_quantity_dict

    exists = os.path.isfile("./book_log.xlsx")

    if exists:
        data = pd.read_excel("./book_log.xlsx")
    else:
        data = pd.DataFrame(columns=["Item Name", "Description", "Category",
                                     "SKU", "Variation Name", "Price", "Current Quantity Groundwork Books",
                                     "New Quantity Groundwork Books", "Stock Alert Enabled Groundwork Books",
                                     "Stock Alert Count Groundwork Books", "Tax - Sales Tax (7.75%)"])

    ISBN_quantity_dict = dict(zip(data["SKU"], data["New Quantity Groundwork Books"] + data["Current Quantity Groundwork Books"].fillna(0)))

    return data


def merge_book(ISBN, data):
    in_log = False
    quantity = 1

    # check if book is in book_log.xlsx
    ISBN = int(ISBN)
    if ISBN in ISBN_quantity_dict:
        if math.isnan(data.loc[data["SKU"] == ISBN, "New Quantity Groundwork Books"]):
            data.loc[data["SKU"] == ISBN, "New Quantity Groundwork Books"] = 0
            ISBN_quantity_dict[ISBN] = 0
        ISBN_quantity_dict[ISBN] += 1
        in_log = True

        data.loc[data["SKU"] == ISBN, "New Quantity Groundwork Books"] += 1
        quantity = data.loc[data["SKU"] == ISBN, "New Quantity Groundwork Books"]

    return quantity, in_log, data


def update_price(data, ISBN, price):
    data.loc[data["SKU"] == ISBN, "Price"] = price
    return data


def web_log(ISBN, data, vol, category):
    output = vol.list(q="isbn:" + ISBN, maxResults=1).execute()
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
            print("The ISBN number you typed in is ISBN 10, not ISBN13. There is no ISBN13 number in database for "
                  "this book.")
            ISBN_in = input("Enter ISBN 13 manually: ").strip()
            if ISBN_in:
                ISBN = ISBN_in

    quantity, in_log, data = merge_book(ISBN, data)
    if in_log:
        print("Already in inventory, new quantity increased from {} to {}".format(ISBN_quantity_dict[int(ISBN)] - 1,
                                                                                  ISBN_quantity_dict[int(ISBN)]))
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
        ISBN_quantity_dict[int(ISBN)] = 1
        data = data.append({"Item Name": title, "Description": publisher, "Category": category, "SKU": int(ISBN),
                            "Variation Name": author, "Price": float(price), "Current Quantity Groundwork Books": "",
                            "New Quantity Groundwork Books": 1, "Stock Alert Enabled Groundwork Books": "",
                            "Stock Alert Count Groundwork Books": "", "Tax - Sales Tax (7.75%)": "Y"},
                           ignore_index=True)

    return data


def main():
    with open("key.txt", "r") as f:
        api_key = f.readline().strip()
    service = build("books", "v1", developerKey=api_key)
    vol = service.volumes()
    category = ""
    data = update_books()
    try:
        while True:
            # data = update_books()
            num = input("Enter the ISBN, or enter category:category name to set the category. "
                        "If finished, type \'quit\': ").strip()
            if num == "quit":
                break
            if num.startswith("category:"):
                category = num[9:].strip()
                print("Category set to \"" + category + "\"")
            elif num.strip() != "":
                data = web_log(num, data, vol, category)
    finally:
        print("Writing to file...")
        data.to_excel("book_log.xlsx", index=False)
        print("Done writing")


if __name__ == "__main__":
    main()

# with open("key.txt", "r") as f:
#     api_key = f.readline().strip()
# service = build("books", "v1", developerKey=api_key)
# vol = service.volumes()
# # print(vol)
# output = vol.list(q="isbn:9781583671535", maxResults=1).execute()
# print(output["items"][0])
