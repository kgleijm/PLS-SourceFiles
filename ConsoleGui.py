import warnings
from abc import ABC, abstractmethod

# method to clear the terminal
def clearTerminal():
    print("\n" * 100)

#   method that will create a choice dialog
def openQuestionChecked(question, checks=None, negativeResponse=None):

    output = ""

    #   base output if no checks or negative response are needed
    if checks is None and negativeResponse is None:
        #   just return answer
        print("\n" + question)
        output = input()
        return output

    #   interpret question when checks are given
    else:
        #   Keep asking the same question until checks are met or user exits
        print("\n" + question)
        print("type exit if you don't know")
        while True:
            output = input()

            #   escape if satisfactory answer is unknown
            if output == "exit":
                return "ERROR"

            #   loop through the checks
            satisfactory = True
            for check in checks:
                if check not in output:
                    satisfactory = False

            # act based on the outcome of these checks
            if satisfactory:
                return output
            elif negativeResponse is not None:
                print("\n" + negativeResponse)
                print("Try again or type exit if you don't know")
            else:
                print("\nThat's not right, try again or type exit if you don't know")

#   shorthand way of coding above question
def openQuestion(question):
    return openQuestionChecked(question, None, None)

# method that returns an int corresponding to a given answer
def multipleChoice(question, *inp_options):

    # failsafe for elementByMultiplechoice
    options = list()
    if type(inp_options[0]) is list:
        for e in inp_options[0]:
            options.append(e)
    else:
        options = inp_options

    print("\n" + question)
    while True:
        # ask question and prepare for answers
        possibleAnswers = []
        for i, option in enumerate(options):

            # count how many numeral chars are in this possible answer to account for inputs beginning with numbers
            lengthOfExpectedUserInput = 1
            for j in range(len(option)):
                if not option[j].isdigit():
                    break
                elif j+1 > lengthOfExpectedUserInput:
                    lengthOfExpectedUserInput = j+1


            # distill info
            newAns = option[0:lengthOfExpectedUserInput].upper()
            firstChar = option[lengthOfExpectedUserInput:lengthOfExpectedUserInput+1].upper()
            listOption = "[" + newAns + "]" + " " + firstChar + option[lengthOfExpectedUserInput+1:len(option)]

            # list options and save answer
            possibleAnswers.append(newAns)
            print(listOption)

        # add exit for escape
        print("[X] Exit\n")

        # get answer
        ans = input().upper()

        # check answer
        if ans == "X":
            return -1
        else:
            for i in range(len(possibleAnswers)):
                if ans == possibleAnswers[i]:
                    return i
        print("that's not an option, type \"X\" if you don't know")

# method that returns an int based on a question
def getInt(question):
    print(question)
    while True:
        ans = input()
        output = 0
        if ans == "exit":
            return -1
        try:
            return int(ans)
        except:
            print("that is not a valid answer, try again or type exit to exit")

# checks if there are no errors in answers #TODO write method
def noErrorsInValues():
    pass

class Element(ABC):

    def __init__(self):
        self.key = ""

    def list(self):
        pass

    def getMPQlisting(self):
        pass

    def setKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

def getElementByMultipleChoice(question, input):
    # print(type(input))
    if type(input) is list:
        answers = list()
        for i in range(len(input)):
            answers.append(str(i) + str(input[i].getMPQlisting()))
        multipleChoice(question, answers)
    elif type(input) is dict:
        return getElementByMultipleChoice(question, list(input.values()))
    else:
        print("ERROR: not a valid iterable for multiplechoice")

# get values bij vararg list, first element in list is the value, additional elements are options for if the question should be a multiple choice
# question will be recycled for every value
# answers will be strings
def getDictOfValuesByMultipleChoice(question, *inp_valueLists):
    valsDict = dict()

    for valueList in inp_valueLists:
        # valueList[0] will be type of question:
            # o = openQuestion,
            # c = openQuestionChecked with varargs used as checks,
            # m = multipleChoice with varargs used as options
            # i = getInt
        # valueList[1] will be the value name that will be used as a key in the dict

        if valueList[0] == 'o':
            # openQuestion
            valsDict[valueList[1]] = openQuestion(question + ' ' + valueList[1])
        elif valueList[0] == 'm':
            # multipleChoice
            valsDict[valueList[1]] = multipleChoice(question + ' ' + valueList[1], valueList[2:])
        elif valueList[0] == 'c':
            # openQuestionChecked
            valsDict[valueList[1]] = openQuestionChecked(question + ' ' + valueList[1], valueList[2:])
        elif valueList[0] == 'i':
            # getInt
            valsDict[valueList[1]] = openQuestionChecked(question + ' ' + valueList[1], valueList[2:])
        else:
            raise Exception('getDictOfValuesByMultipleChoice() encountered invalid question form')



class Class(Element, ABC):

    # Data structures to hold objects of this class(static)
    objectDict = dict()
    objectList = list()

    # call in __init__ child object to set "variables" used in child class
    # "variables" are  key value pairs
    def __init__(self, **vars):
        # Data structure to hold variables (non-static)
        self.variableDict = vars

    @abstractmethod
    def getMPQlisting(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get(self, variableName):
        pass

    @abstractmethod
    def set(self, variableName, value):
        pass

    def getListOfObjectsWithValue(self, variable, value):
        output = list()
        for ob in type(self).objectDict:
            if ob.variableDict[variable] == value:
                output.append(ob)
        return output

class StateEngine:
    # class that contains an action and description of the state to
    # minimize boilerplate code
    class State:

        def __init__(self, inp_func, inp_description):
            self.func = inp_func
            self.desc = inp_description

        def run(self):
            self.func()

        def getDescription(self):
            return self.desc

    # static state variables
    safeState = None
    stateStack = []
    currentState = None
    running = False

    # currentState will be set to this state when an unexpected end of the stateStack hes been found
    @staticmethod
    def setSafeState(inp_safeState):
        StateEngine.stateStack.clear()
        StateEngine.safeState = inp_safeState

    # goes back one state in the stack
    @staticmethod
    def getPreviousState():
        if StateEngine.stateStack:
            return StateEngine.stateStack.pop()
        elif StateEngine.safeState:
            warnings.warn("defaulted to safeState")
            return StateEngine.safeState
        else:
            StateEngine.stop()
            raise Exception('Unexpected end of stateStack in getPreviousState (no safeState set)')

    # push state to stack without executing it
    @staticmethod
    def pushStateToStack(inp_state):
        StateEngine.stateStack.append(inp_state)

    # starts the state engine
    @staticmethod
    def start():
        StateEngine.running = True
        while StateEngine.running:
            StateEngine.currentState.run()

    # stops the state engine
    @staticmethod
    def stop():
        StateEngine.running = False

    #  set new state
    @staticmethod
    def setState(newState, stacked=True):
        StateEngine.currentState = newState
        if stacked:
            StateEngine.stateStack.append(newState)
        if not StateEngine.running:
            StateEngine.start()

    # go to previous stacked state
    @staticmethod
    def setStateToPrevious():
        StateEngine.setState(StateEngine.getPreviousState(), stacked=False)

    # prompt user with a multiple choice of state descriptions
    @staticmethod
    def setStateByMultipleChoice(question, default, *states):
        index = multipleChoice(question, [str(state[0]) + state[1].getDescription() for state in enumerate(states)])
        if index is not -1:
            StateEngine.setState(states[index])
        elif default:
            StateEngine.setState(default)
        else:
            StateEngine.setState(StateEngine.getPreviousState())

class DataManager:
    # dict that holds all dicts of registered objects accessed by key:
    typeDict = dict()
    lastUniqueKey = 0

    # function that adds element to its own dict and if it doesn't exist, creates that dict
    @staticmethod
    def addByKey(key, inp_element):
        inp_type = type(inp_element)
        if inp_type in DataManager.typeDict:
            DataManager.typeDict[inp_type][str(key)] = inp_element
        else:
            print('data type: ' + str(inp_type) + 'added to DataManager')
            DataManager.typeDict[inp_type] = dict()
            DataManager.typeDict[inp_type][str(key)] = inp_element
        inp_element.setKey(str(key))

    @staticmethod
    def add(inp_element):
        DataManager.addByKey(DataManager.getUniqueKey(inp_element), inp_element)

    # Generate unique keys for elements
    @staticmethod
    def getUniqueKey(inp_element):
        inp_type = type(inp_element)
        if inp_type in DataManager.typeDict:
            while str(DataManager.lastUniqueKey) in DataManager.typeDict[inp_type]:
                DataManager.lastUniqueKey += 1
            return str(DataManager.lastUniqueKey)
        else:
            DataManager.lastUniqueKey += 1
            return str(DataManager.lastUniqueKey)

    # returns ConsoleGui Element from dict
    @staticmethod
    def ChooseElementInDictOfTypeFrom(question, inp_element):
        inp_type = type(inp_element)
        print('Datamanager tries to make a list of: ' + str(inp_type))
        if inp_type in DataManager.typeDict:
            return getElementByMultipleChoice(question, DataManager.typeDict[inp_type])
        else:
            print("no dict of element-type found")
            return None

    # Removes ConsoleGui Element from dict
    @staticmethod
    def RemoveElementInDictOfTypeFrom(question, inp_element):
        element = DataManager.ChooseElementInDictOfTypeFrom(question, inp_element)
        if element == None:
            return "ERROR"
        else:
            removeKey = element.getKey()
            inp_type = type(element)
            del DataManager.typeDict[inp_type][removeKey]