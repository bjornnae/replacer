# identifyCandidates.py

"""
If candidates for replacement can be defined by regexp,
"""

import re
import gdeserializer

statisticsDict = {"filesSearched": 0, "linesSearched" : 0, "matchInstances": {}}

def findInLine(regexp, line):
    result = re.findall(regexp, line)
    return ( result )


def findInFile(filePath, regexpList):
    fh = open(filePath, "r")
    statisticsDict["filesSearched"] += 1
    lines = fh.readlines()
    fh.close()
    matches = []
    lineNumber = 0
    for l in lines:
        statisticsDict["linesSearched"] += 1
        lineNumber += 1
        for re in regexpList:
            match = findInLine(re, l)
            #print("debug: %s@%s => %s" % (re, l, match))
            if match != []:
                for m in match:
                    if statisticsDict["matchInstances"].has_key(m):
                        statisticsDict["matchInstances"][m] += 1
                    else:
                        statisticsDict["matchInstances"][m] = 1
                matches.append([filePath + ":" + str(lineNumber), match])
    return(matches)


def findInFiles(filePathList, regexpList):
    result = []
    for f in filePathList:
        result += findInFile(f, regexpList)
    return (result)

#
#def parseRegexpListFromFile(filePath):
#    regexplist = gdeserializer.parseListFromFile(filePath)
#    for r in regexplist:
#        try:
#            a = re.compile(r)
#            regexpList.append(r)
#
#    return( regexpList )


if __name__ == "__main__":
    regexpList = gdeserializer.parseRegexpListFromFile("./conf/replaceCandidateRegexps.txt")
    fileList = gdeserializer.parseListFromFile("./conf/replaceInFiles.txt")
    #result = findInFiles(["./conf/testfiles/conf1.dat", "./conf/testfiles/conf2.dat"], regexpList)
    result = findInFiles(fileList, regexpList)
    print(statisticsDict)
    print("-------")
    print(result)
