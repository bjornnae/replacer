# identifyCandidates.py

"""
If candidates for replacement can be defined by regexp, 
"""

import re
import gdeserializer

def findInLine(regexp, line):
    result = re.findall(regexp, line)
    return ( result )


def findInFile(filePath, regexpList):
    fh = open(filePath, "r")
    lines = fh.readlines()
    fh.close()
    matches = []
    lineNumber = 0
    for l in lines:
        lineNumber += 1
        for re in regexpList:
            match = findInLine(re, l)
            if match != []:
                matches.append([filePath + ":" + str(lineNumber), match])
    return(matches)
    
    
def findInFiles(filePathList, regexpList):
    result = []
    for f in filePathList:
        result += findInFile(f, regexpList)
    return (result)


def parseRegexpListFromFile(filePath):
    regexplist = gdeserializer.parseListFromFile(filePath)
    for r in regexplist:
        try:
            a = re.compile(r)
            regexpList.append(r)
                
    return( regexpList )
            
        
if __name__ == "__main__":
    regexpList = parseRegexpListFromFile("./conf/replaceCandidateRegexps.txt")
    #result = findInFiles(["./conf/testfiles/conf1.dat", "./conf/testfiles/conf2.dat"], ['Server\-[A-Z]{1}', 'server\-[a-z]*'])
    result = findInFiles(["./conf/testfiles/conf1.dat", "./conf/testfiles/conf2.dat"], regexpList)
    print(result)