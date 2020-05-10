import csv
import json
import os

# print json
def printJson(inp_json):
    for e in inp_json:
        print(e)

# get json from web method
def getJsonFromPath(path):
        with open(path) as inp_json:
            data = json.load(inp_json)
            return data

# save json at path method
def saveJsonAtPath(path, filename, outputJson):
    with open(path + '\\' + filename + '.json', 'w') as outfile:
        json.dump(outputJson, outfile)

# get csv from web or path method
def getCsvAsList(adress, delimiter):
    output = list()
    # print('\n')
    # print('try to get csv from local path: ' + adress)
    f = open(adress, 'r')
    reader = csv.reader(f, delimiter=delimiter)
    for row in reader:
        # print('found row:' + str(row))
        thisRow = list()
        for e in row:
            thisRow.append(e)
        output.append(thisRow)
    f.close()
    # print('\n')
    return output

# save csv at path method
def saveAsCsvAtPath(adress, filename, iterable):

    outpath = adress + '\\' + filename + '.csv'
    print('\n jcsvHandler will try to save at' + outpath)

    try:
        os.mkdir(adress)
        print('made directory ' + adress)
    except FileExistsError:
        print('directory does already exist, will write to existing file')

    try:
        f = open(outpath, 'w')
        writer = csv.writer(f)
        writer.writerows([iterable])
        f.close()
        return outpath
    except PermissionError:
        print("cant write to file, might already be open somewhere\n")

# save and load text at path
def saveTextAtPath(path, filename, string):
    try:
        os.mkdir(path)
        print('directory created')
    except:
        pass
    with open(path + '\\' + filename + '.txt', 'w') as outfile:
        outfile.write(string)

# get text from path as string
def getTextFromPath(path):
    with open(path) as f:
        return str(f.readlines())

# generate folder structure
def generateFolderStructure(basePath, baseFolderName,*folders):

    basefolder = os.path.join(basePath, baseFolderName)
    try:
        os.mkdir(basefolder)
        print("made folder: " + basefolder)
    except Exception as e:
        pass
        # print("failed generating baseFolder\n" + str(e))

    for folder in folders:
        # if list:   recursively unpack list to make new level(s) in folder structure
        # first string in the list will decide name of new baseMap, following strings  wil name sub-folders
        # sub-folders can have lists as well to add another layer
        if type(folder) is list:
            newBaseFolder = folder[0]
            subFolders = folder[1:]
            generateFolderStructure(basefolder, newBaseFolder, *subFolders)
        else:
            try:
                newfolder = os.path.join(basefolder, folder)
                os.mkdir(newfolder)
                print("made folder: " + newfolder)
            except Exception as e:
                pass
                # print("failed generating folderStructure: " + folder + "\n" + str(e))
    return basefolder

def getFolderByName(basePath, folder):
    for e in os.walk(basePath, topdown=True):
        if e[0].split('\\')[-1] == folder:
            print('found: ' + folder)
            return folder
    print('folder not found')
    return None

