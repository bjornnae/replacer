#!/bin/env python


import gdeserializer
import os
import re

replaceStringList = "./conf/replaceMap.txt"
replaceFileList = "./conf/replaceInFiles.txt"
replacedFileSuffix = ".modified"
originalFileSuffix = ".original"

def parseFilePathFile(filePath):
    resultLines = gdeserializer.parseListFromFile(filePath)
    return resultLines
    
def parseReplaceExpressions(filePath):
    replaceMap = gdeserializer.parseHashMapFromFile(filePath)
    return replaceMap
    
    
def validateReplaceMap(replaceMap):
    # "Verify that no keys exist in replacement values."
    testPassed = True
    for k1 in replaceMap:
        for k2 in replaceMap:
            if re.findall(k1, replaceMap[k2]) != []:
                print("Violating replacement map check: key '%s' is also in a replacement pattern ('%s')." % (k1, replaceMap[k2]))
                testPassed = False
    return(testPassed)
            
def replaceInFiles(filePathList, replaceMap):
    
    # Pre perform check:
    if validateReplaceMap(replaceMap):
        for f in filePathList:
            originalFilePath = f + originalFileSuffix
            
            with open(f, "r") as fh:
                fcontent = fh.read()
            
            with open(originalFilePath, "w+") as fhO:
                fhO.write(fcontent)
            
            for k in replaceMap:
                # Make replacement step here. Modifies fcontent.
                fcontent = fcontent.replace(k, replaceMap[k])
                print ("Replacing %s -> %s" % ( k, replaceMap[k])) 
            
            modifiedFilePath = f + replacedFileSuffix
            with open(modifiedFilePath, "w+") as fhM:
                fhM.write(fcontent)
        return (True)
    else:
        print("No replacement activites were performed.")
        return (False)
        
if __name__ == "__main__":
    
    fileList = parseFilePathFile(replaceFileList)
    print("DEBUG:>> %s" % (fileList))
    replaceExpressions = parseReplaceExpressions(replaceStringList)
    print("DEBUG:>> %s" % (replaceExpressions))
    replaceInFiles(fileList, replaceExpressions)
    