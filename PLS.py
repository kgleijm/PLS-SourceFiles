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

# classes
class ImportExportManager:
    setUp = False

    root = str(__file__).replace("PLS.py", "")
    baseBookSetFilePath = root + "booksset1.json"
    baseUserSetFilePath = root + "FakeNameSet20.csv"
    dictOfAuthors = dict()
    dictOfCountries = dict()
    dictOfLanguages = dict()


    @staticmethod
    def setup():
        ImportExportManager.importData()
        ImportExportManager.processData()
        DataManager.addByKey('admin', User('admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', 'admin', User.ROLE_ADMIN))

    @staticmethod
    def importData():
        IEM = ImportExportManager
        IEM.bookJson = jcsv.getJsonFromPath(IEM.baseBookSetFilePath)
        IEM.userCsv = jcsv.getCsvAsList(IEM.baseUserSetFilePath, ',')

    @staticmethod
    def processData():
        print("loading books")
        for book in ImportExportManager.bookJson:
            key = book['title']
            DataManager.addByKey(key, Book(book['author'], book['country'], book['language'], book['pages'], book['title'], book['year'], inp_amount=1))
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

    # used for multipleChoice'ing keys
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

    def isAvailable(self):
        return self.amount > 0

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
        return Book(None, None, None, None, 'None', None)


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
        return User(None, None, 'None', None, None, None, None, None, None, None, None)


class BookLoan(cg.Element):

    def __init__(self, inp_user, inp_book):
        super().__init__()
        key = inp_user.name + inp_book.title
        self.user = inp_user
        self.book = inp_book
        self.book.loanBook()
        DataManager.addByKey(key, self)
        self.setKey(key)

    def getMPQlisting(self):
        return self.user.name + ' loaned ' + self.book.title

    def list(self):
        print(self.getMPQlisting())

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def getName(self):
        return self.user.name

    def returnLoan(self):
        self.book.returnBook()
        DataManager.removeWithKeyFromType(self.key, BookLoan.getNoneLoan())




    @staticmethod
    def getNoneLoan():
        return BookLoan(User.getNoneUser(), Book.getNoneBook())

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
        StateEngine.setStateByMultipleChoice('What would you like to do?', STATE_MAIN, STATE_ADD_BOOK, STATE_SEARCH_BOOK, STATE_DISPLAY_LOANS)
STATE_LOGGED_IN = State(stateLoggedIn, 'Go to Main menu')


def stateMakeLoan():
    global gActiveUser, gActiveBook

    # make the state work for both librarian and user
    if gActiveBook.isAvailable():
        if gActiveUser.role == User.ROLE_ADMIN:
            subjectUser = cg.getElementByMultipleChoice('for which user should the loan be made? ', User.getNoneUser())
        else:
            subjectUser = gActiveUser
        # make a bookLoanItem with key: user + title
        BookLoan(subjectUser, gActiveBook)
        StateEngine.setStateByMultipleChoice('Book loan is succesfully made, what would you like to do next?', STATE_LOGGED_IN, STATE_SEARCH_BOOK, STATE_INTERACT_WITH_BOOK, STATE_RETURN_BOOK)
    else:
        StateEngine.setStateByMultipleChoice("this book is unavailable, what would you like to do?", STATE_LOGGED_IN, STATE_SEARCH_BOOK, STATE_INTERACT_WITH_BOOK)
STATE_MAKE_LOAN = State(stateMakeLoan, 'Make a book loan')


def stateInteractWithBook():
    global gActiveUser
    print('Book info: ' +
          '\nTitle: ' + gActiveBook.title +
          '\nAuthor: ' + gActiveBook.author +
          '\nCountry: ' + gActiveBook.country +
          '\nLanguage: ' + gActiveBook.language +
          '\nPages: ' + str(gActiveBook.pages) +
          '\nYear: ' + str(gActiveBook.year) +
          '\n'
          )
    if gActiveUser.role == User.ROLE_USER:
        StateEngine.setStateByMultipleChoice("what would you like to do?", STATE_LOGGED_IN, STATE_MAKE_LOAN, STATE_SEARCH_BOOK)
    else:
        StateEngine.setStateByMultipleChoice("what would you like to do?", STATE_LOGGED_IN, STATE_ADD_BOOK, STATE_SEARCH_BOOK)
STATE_INTERACT_WITH_BOOK = State(stateInteractWithBook, 'check out book info')


def stateDisplayAllBookLoans():
    print('All current loans:')
    loanList = DataManager.getDictOfType(BookLoan.getNoneLoan()).values()
    for loan in loanList:
        loan.list()
    StateEngine.setState(STATE_LOGGED_IN)
STATE_DISPLAY_LOANS = State(stateDisplayAllBookLoans, 'Display current outstanding loans')


def stateMain():
    global gActiveUser
    if gActiveUser is not None:
        gActiveUser = None
    StateEngine.setStateByMultipleChoice("What would you like to do?", STATE_EXIT, STATE_LOG_IN, STATE_CREATE_ACCOUNT)
STATE_MAIN = State(stateMain, "Home")


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
    global gActiveUser
    if gActiveUser.role == User.ROLE_ADMIN:
        subjectUser = cg.getElementByMultipleChoice('for which user should a return be made? ', User.getNoneUser())
    else:
        subjectUser = gActiveUser

    # get all loans for subjectUser
    loanList = list()
    for loan in DataManager.getDictOfType(BookLoan.getNoneLoan()).values():
        if loan.getName() == subjectUser.name:
            loanList.append(loan)

    rLoan = cg.getElementByMultipleChoice('which book would you like to return?', loanList)
    if rLoan is None:
        print('something went wrong while returning a book')
        StateEngine.setState(STATE_LOGGED_IN)
    else:
        rLoan.returnLoan()
        StateEngine.setStateByMultipleChoice('Book is succesfully returned, what would you like to do next?', STATE_LOGGED_IN, STATE_SEARCH_BOOK, STATE_INTERACT_WITH_BOOK, STATE_RETURN_BOOK)
STATE_RETURN_BOOK = State(stateReturnBook, 'Return a book')


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



# Main
ImportExportManager.setup()
StateEngine.setSafeState(STATE_MAIN)
StateEngine.setState(STATE_MAIN)
