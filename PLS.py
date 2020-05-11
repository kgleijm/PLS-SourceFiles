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
gActiveBook = None
gActiveBookItem = None

# global methods
def setActiveUser(inp_user):
    global gActiveUser
    gActiveUser = inp_user



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

    # TODO make json for author (obsolete)

    # TODO make json for bookItem

    # TODO make json for User

    @staticmethod
    def setup():
        ImportExportManager.importData()
        ImportExportManager.processData()

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
            DataManager.addByKey(book['title'], Book(book['author'], book['title'], book['country'], book['language'], book['pages'], book['year']))

        print("loading users")
        # 0'20', 1'female', 2'Dutch', 3'GÃ¼lseren', 4'Willigenburg', 5'Dingspelstraat 28', 6'9461 JE', 7'Gieten', 8'GulserenWilligenburg@teleworm.us', 9'Ressoare', 10'06-92433659'
        # 1inp_gender, 2inp_language, 3inp_name, 4inp_surname, 5inp_adress, 6inp_postalCode, 76inp_city, 8inp_email, 9inp_username, 10inp_telephoneNumber
        for userElement in ImportExportManager.userCsv:
            # print('adding user: ' + str(userElement[9]))
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


class Book(cg.Element):
    def __init__(self, inp_author, inp_title, inp_country, inp_language, inp_pages, inp_year):
        super().__init__()
        self.author = inp_author
        self.title = inp_title
        self.country = inp_country
        self.language = inp_language
        self.pages = inp_pages
        self.year = inp_year

    def getMPQlisting(self):
        return self.title + ' by ' + self.author

    def list(self):
        print(self.getMPQlisting())

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    @staticmethod
    def getNoneBook():
        return Book(None, None, None, None, None, None)


class BookItem(cg.Element):

    def getMPQlisting(self):
        pass

    def list(self):
        pass

    def setKey(self, key):
        pass

    def getKey(self):
        pass


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

STATE_CREATE_ACCOUNT = State(stateCreateAccount, 'create an account')


def stateLoggedIn():
    print('state logged in')
STATE_LOGGED_IN = State(stateLoggedIn, 'Go to Main menu')



def stateMain():
    global gActiveUser
    if gActiveUser is not None:
        gActiveUser = None
    StateEngine.setStateByMultipleChoice("What would you like to do?", STATE_EXIT, STATE_LOG_IN, STATE_CREATE_ACCOUNT)
STATE_MAIN = State(stateMain, "Home")



# Main
ImportExportManager.setup()
StateEngine.setSafeState(STATE_MAIN)
StateEngine.setState(STATE_MAIN)
