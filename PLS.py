# imports
import os
import ConsoleGui as cg
import jcsvHandler as jcsv

# tools
DataManager = cg.DataManager
StateEngine = cg.StateEngine
State = StateEngine.State

# globals
gActiveUser = None
def setActiveUser(inp_user):
    global gActiveUser
    gActiveUser = inp_user

gActiveBook = None
def setActiveBook(inp_book):
    global gActiveBook
    gActiveBook = inp_book

# global methods




# classes
class ImportExportManager:
    setUp = False

    root = str(__file__).replace("PLS.py", "")
    print(root)
    baseBookSetFilePath = root + "booksset1.json"
    alteredBookSetFilePath = root + "alteredBooksSet.json"
    bookJson = None

    baseUserSetFilePath = root + "FakeNameSet20.csv"
    alteredUserSetFilePath = root + "alteredUserSet.csv"
    userCsv = None

    dictOfAuthors = dict()
    dictOfCountries = dict()
    dictOfLanguages = dict()

    # TODO make json for bookLoan

    # TODO make csv for User

    @staticmethod
    def setup():
        ImportExportManager.importData()
        ImportExportManager.processData()
        DataManager.addByKey('admin', User('admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', User.ROLE_ADMIN))

    @staticmethod
    def importData():
        IEM = ImportExportManager

        # import altered book set if it exists import base set if it doesn't
        if os.path.exists(IEM.alteredBookSetFilePath):
            IEM.bookJson = jcsv.getJsonFromPath(IEM.alteredBookSetFilePath)
        else:
            IEM.bookJson = jcsv.getJsonFromPath(IEM.baseBookSetFilePath)

        # import altered user set if it exists import base set if it doesn't
        if os.path.exists(IEM.alteredUserSetFilePath):
            IEM.userCsv = jcsv.getCsvAsList(IEM.alteredUserSetFilePath)
        else:
            IEM.userCsv = jcsv.getCsvAsList(IEM.baseUserSetFilePath, ',')

    @staticmethod
    def processData():
        print("loading books")
        for book in ImportExportManager.bookJson:
            key = book['title']
            DataManager.addByKey(key, Book(book['author'], book['country'], book['language'], book['pages'], book['title'], book['year']))
            if not book['author'] in ImportExportManager.dictOfAuthors:
                ImportExportManager.dictOfAuthors[book['author']] = True
            if not book['country'] in ImportExportManager.dictOfCountries:
                ImportExportManager.dictOfCountries[book['country']] = True
            if not book['language'] in ImportExportManager.dictOfLanguages:
                ImportExportManager.dictOfLanguages[book['language']] = True

        print("loading users")
        for userElement in ImportExportManager.userCsv:
            DataManager.addByKey(userElement[9], User(userElement[1], userElement[2], userElement[3], userElement[4], userElement[5], userElement[6], userElement[7], userElement[8], userElement[9], userElement[10], User.ROLE_USER))

    @staticmethod
    def printAllBookData():
        if not ImportExportManager.setUp:
            ImportExportManager.setup()
        for book in ImportExportManager.bookJson:
            print(book)

    @staticmethod
    def printAllUserData():
        if not ImportExportManager.setUp:
            ImportExportManager.setup()
        for user in ImportExportManager.userCsv:
            print('úser[2] should be: ' + user[2])

    # used for multipleChoiceing keys
    class keyElement(cg.Element):
        def __init__(self, inp_Key):
            super().__init__()

        def getMPQlisting(self):
            pass

        def list(self):
            pass

        def setKey(self, key):
            pass

        def getKey(self):
            pass


class Book(cg.Element):
    def __init__(self, inp_author, inp_country, inp_language, inp_pages, inp_title, inp_year, inp_amount=1):
        super().__init__()
        self.author = inp_author
        self.title = inp_title
        self.country = inp_country
        self.language = inp_language
        self.pages = inp_pages
        self.year = inp_year
        self.amount = inp_amount

    def getMPQlisting(self):
        return str(self.title) + '       by ' + str(self.author) + '          amount available: ' + str(self.amount)

    def list(self):
        print(self.getMPQlisting())

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getAuthor(self):
        return self.author

    def getCountry(self):
        return self.country

    def getLanguage(self):
        return self.language



    def loanBook(self):
        if self.amount > 0:
            self.amount -= 1
            return True
        else:
            return False

    def returnBook(self):
        self.amount += 1

    @staticmethod
    def getNoneBook():
        return Book(None, None, None, None, None, None)


class User(cg.Element):
    ROLE_USER = 0
    ROLE_ADMIN = 1

    def __init__(self, inp_gender, inp_language, inp_name, inp_surname, inp_adress, inp_postalCode, inp_city, inp_email, inp_username, inp_telephoneNumber, inp_role):
        super().__init__()
        self.gender = inp_gender
        self.language = inp_language
        self.name = inp_name
        self.surname = inp_surname
        self.adress = inp_adress
        self.postalCode = inp_postalCode
        self.city = inp_city
        self.email = inp_email
        self.username = inp_username
        self.telephoneNumber = inp_telephoneNumber
        self.role = inp_role

    def getMPQlisting(self):
        return self.username + ' (' + self.name + ' ' + self.surname + ')'

    def list(self):
        print(self.getMPQlisting())

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    @staticmethod
    def getNoneUser():
        return User(None, None, None, None, None, None, None, None, None, None, None)



"""
class BookLoan(cg.Element):



    def getMPQlisting(self):
        pass

    def list(self):
        pass

    def setKey(self, key):
        pass

    def getKey(self):
        pass

class BookItem(cg.Element):

    def getMPQlisting(self):
        pass

    def list(self):
        pass

    def setKey(self, key):
        pass

    def getKey(self):
        pass
"""

""" state declaration template
def state():
    pass    
STATE_ = State(state, 'desc')
"""



# states
def stateLogin():
    global gActiveUser
    StateEngine.clearStateStack()
    while True:
        potentialUserName = cg.openQuestion('what is your username?')
        # check if not exit
        if potentialUserName is 'ERROR':
            if gActiveUser:
                StateEngine.setState(STATE_LOGGED_IN)
            else:
                StateEngine.setState(STATE_MAIN)
            break
        # check if user exists and handle accordingly
        potentialUser = DataManager.findByKey(potentialUserName, User.getNoneUser())
        if potentialUser:
            setActiveUser(potentialUser)
            StateEngine.setState(STATE_LOGGED_IN)
            break
        else:
            print('No user with that name found')
STATE_LOG_IN = State(stateLogin, 'Log In')


def stateExit():
    print("shutting down, Bye bye!")
    StateEngine.stop()
STATE_EXIT = State(stateExit, 'Exit')


def stateCreateAccount():
    global gActiveUser

    # gather values by user input
    values = cg.getDictOfValuesByValueList(
        'please enter your',
        ['m', 'gender', '1Man', '2Woman', '3Other'],
        ['o', 'name'],
        ['o', 'surname'],
        ['o', 'street and house number'],
        ['o', 'postal code'],
        ['o', 'city'],
        ['c', 'email', '@', '.'],
        ['o', 'userName'],
        ['i', 'telephoneNumber']
        )

    # generate user object and add to DataManager
    newUser = User(values['gender'],
          'Dutch',
          values['name'],
          values['surname'],
          values['street and house number'],
          values['postal code'],
          values['city'],
          values['email'],
          values['userName'],
          values['telephoneNumber'],
          User.ROLE_USER)
    DataManager.addByKey(values['userName'], newUser)

    # new account creation
    if gActiveUser is None:
        gActiveUser = newUser
    StateEngine.setState(STATE_LOGGED_IN)
STATE_CREATE_ACCOUNT = State(stateCreateAccount, 'Create an account')


def stateLoggedIn():
    print('Hi ' + gActiveUser.name + ', welcome To the PLS System')
    if gActiveUser.role == User.ROLE_USER:
        StateEngine.setStateByMultipleChoice('What would you like to do?', STATE_MAIN, STATE_SEARCH_BOOK, STATE_RETURN_BOOK)
    else:
        StateEngine.setStateByMultipleChoice('What would you like to do?', STATE_MAIN, STATE_ADD_BOOK, STATE_SEARCH_BOOK)
STATE_LOGGED_IN = State(stateLoggedIn, 'Go to Main menu')

def stateInteractWithBook():
    print('Book info: ' +
          '\nTitle: ' + gActiveBook.title +
          '\nAuthor: ' + gActiveBook.author +
          '\nCountry: ' + gActiveBook.country +
          '\nLanguage: ' + gActiveBook.language +
          '\nPages: ' + str(gActiveBook.pages) +
          '\nYear: ' + str(gActiveBook.year) +
          '\n'
          )

    StateEngine.setStateByMultipleChoice("what would you like to do?", STATE_LOGGED_IN, 'lloan this book', STATE_SEARCH_BOOK)



STATE_INTERACT_WITH_BOOK = State(stateInteractWithBook, 'check out book')

def stateMakeLoan():
    pass
STATE_ = State(stateMakeLoan(), 'desc')

def stateMain():
    global gActiveUser
    if gActiveUser is not None:
        gActiveUser = None
    StateEngine.setStateByMultipleChoice("What would you like to do?", STATE_EXIT, STATE_LOG_IN, STATE_CREATE_ACCOUNT)
STATE_MAIN = State(stateMain, "Home")


# userStates
def stateSearchBook():
    global gActiveBook
    activeBook = Book.getNoneBook()
    ans = cg.multipleChoice("How would you like to find your book?", '0search all books', '1find a book by property')


    if ans == -1:
        StateEngine.setState(STATE_LOGGED_IN)
    elif ans == 0:
        # search all books
        activeBook = DataManager.ChooseElementInDictOfTypeFrom('choose your book:', activeBook)
    elif ans == 1:
        findProperty = cg.multipleChoice('Which property would you like to search on?', 'aauthor', 'ccountry', 'llanguage')
        if findProperty == -1:
            return
        elif findProperty == 0:  # find by author

            # choose the author
            dictkeys = list(ImportExportManager.dictOfAuthors.keys())
            auths = list()
            for i in range(len(dictkeys)):
                auths.append(str(i) + dictkeys[i])
            ans = cg.multipleChoice('by which author do you want to search?', auths)
            auth = ''
            if ans == -1:
                return
            else:
                auth = ''.join([i for i in auths[ans] if not i.isdigit()])


            #choose the book
            bookList = list()
            for book in DataManager.getDictOfType(Book.getNoneBook()).values():
                # print("loop found author: " + book.getAuthor() + " checked against auth: " + auth)
                if book.getAuthor() == auth:
                    bookList.append(book)
            activeBook = cg.getElementByMultipleChoice('which of this authors books would you like to see?', bookList)
            print('Book: ' + activeBook.getMPQlisting())

        elif findProperty == 1:  # find by country

            # choose the country
            dictkeys = list(ImportExportManager.dictOfCountries.keys())
            countries = list()
            for i in range(len(dictkeys)):
                countries.append(str(i) + dictkeys[i])
            ans = cg.multipleChoice('by which country do you want to search?', countries)
            country = ''
            if ans == -1:
                return
            else:
                country = ''.join([i for i in countries[ans] if not i.isdigit()])

            # choose the book
            bookList = list()
            for book in DataManager.getDictOfType(Book.getNoneBook()).values():
                # print("loop found author: " + book.getAuthor() + " checked against auth: " + auth)
                if book.getCountry() == country:
                    bookList.append(book)
            activeBook = cg.getElementByMultipleChoice('which of this county\'s books would you like to see?', bookList)

        elif findProperty == 2:  # find by language

            # choose the language
            print("items: " + str(list(ImportExportManager.dictOfLanguages.keys())))
            dictkeys = list(ImportExportManager.dictOfLanguages.keys())
            languages = list()
            for i in range(len(dictkeys)):
                languages.append(str(i) + dictkeys[i])
            ans = cg.multipleChoice('by which language do you want to search?', languages)
            language = ''
            if ans == -1:
                return
            else:
                language = ''.join([i for i in languages[ans] if not i.isdigit()])

            # choose the book
            bookList = list()
            for book in DataManager.getDictOfType(Book.getNoneBook()).values():
                # print("loop found author: " + book.getAuthor() + " checked against auth: " + auth)
                if book.getLanguage() == language:
                    bookList.append(book)
            activeBook = cg.getElementByMultipleChoice('which of the books in this language would you like to see?', bookList)
            # find by language

    gActiveBook = activeBook
    StateEngine.setState(STATE_INTERACT_WITH_BOOK)
STATE_SEARCH_BOOK = State(stateSearchBook, 'Search a book')

def stateReturnBook():
    pass
# TODO write stateReturnBook()
STATE_RETURN_BOOK = State(stateReturnBook, 'Return a book')


# adminStates
def stateAddBook():
    # gather values by user input
    values = cg.getDictOfValuesByValueList(
        'please enter the',
        ['o', 'author'],
        ['o', 'country'],
        ['o', 'language'],
        ['i', 'amount of pages'],
        ['o', 'title'],
        ['i', 'year']
    )

    # generate user object and add to DataManager
    newBook = Book(values['author'],
                   values['country'],
                   values['language'],
                   values['amount of pages'],
                   values['title'],
                   values['year'])
    DataManager.addByKey(values['title'], newBook)
    print("Added new book: " + values['title'])
    StateEngine.setState(STATE_LOGGED_IN)
STATE_ADD_BOOK = State(stateAddBook, 'Add a book')

"""
def stateMakeSystemBackup():
    pass
STATE_MAKE_BACKUP = State(stateMakeSystemBackup, 'Make a system backup')

def stateRestoreSystemFromBackup():
    pass
STATE_RESTORE_FROM_BACKUP = State(stateRestoreSystemFromBackup, 'Restore system from backup')
"""



# Main
ImportExportManager.setup()
StateEngine.setSafeState(STATE_MAIN)
#TODO debug remove
StateEngine.setState(STATE_SEARCH_BOOK)
StateEngine.setState(STATE_MAIN)
