import os

import ConsoleGui as cg
import jcsvHandler as jcsv

DataManager = cg.DataManager
StateEngine = cg.StateEngine
import json


# classes


class ImportExportManager:
    root = str(__file__).replace("PLS.py", "")
    print(root)
    bookSetFilePath = root + "booksset1.json"
    userSetFilePath = root + "FakeNameSet20.csv"
    alteredBookSetFilePath = root + "alteredBooksSet.json"
    alteredUserSetFilePath = root + "alteredUserSet.csv"
    bookJson = None
    userCsv = None

    @staticmethod
    def importdata():
        if os.path.exists(ImportExportManager.alteredBookSetFilePath):
            ImportExportManager.bookJson = jcsv.getJsonFromPath(ImportExportManager.alteredBookSetFilePath)


    # import baseSet if it exists


    # import new set if updated
        # TODO check for existing files

    """
    @staticmethod
    def printAllBooks():
        for book in bookJson:
            print(book)
    """


class Book(cg.Element):
    def __init__(self, inp_author, inp_title, inp_country, inp_language, inp_pages, inp_year):
        super().__init__()
        self.author = inp_author
        self.title = inp_title
        self.country = inp_country
        self.language = inp_language
        self.pages = inp_pages
        self.year = inp_year


class BookItem(cg.Element):
    pass


class user(cg.Element):
    def __init__(self, name, role):
        super().__init__()

#   Main loop


