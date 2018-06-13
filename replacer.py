#!/bin/env python


import gdeserializer
import os
import sys
import re
import time
import datetime

replaceStringList = "./conf/replaceMap.txt"
replaceFileList = "./conf/replaceInFiles.txt"
replacedFileSuffix = ""
originalFileSuffix = ""

# -- Logging utilities -->
logFile = "./replace.log"

def timestampNow():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return(st)

def appendLog(severity, msg):
	st = timestampNow()
	with open(logFile, "a+") as fh:
		fh.write("\n<%s><%s>%s" % (st, severity, msg))

#<-- end logging

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

def stripCounter(filename):
    try:
        fname, count = ".".join(filename.split(".")[0:-1]), int(filename.split(".")[-1])
        return(fname, count)
    except ValueError:
        return(filename, 0)

def defineNextVersionedFilename(filename):
    print("iterating: %s" % filename)
    if os.path.isfile(filename):
        print("Found file %s. Iterstepping on." % filename)
        fname, count = stripCounter(filename)
        return (defineNextVersionedFilename(fname + "." + str(count + 1)))
    else:
        print("Pleased, found filename that has no file: %s" % filename)
        return(filename)

def defineLastVersionedFilename(filename, previousFilename):
    print("iterating: %s" % filename)
    if os.path.isfile(filename):
        print("Found file %s. Iterstepping on." % filename)
        fname, count = stripCounter(filename)
        return (defineLastVersionedFilename(fname + "." + str(count + 1), filename))
    else:
        print("Pleased, found last version of file: %s" % previousFilename)
        return(previousFilename)


def replaceInFiles(filePathList, replaceMap):

    # Pre perform check:
    if validateReplaceMap(replaceMap):
        for f in filePathList:
            # Backup the original file with a new suffix .original
            # Create a the new file with replaced content. Add suffix .modified to the original filename.

            with open(f, "r") as fh:
                fcontent = fh.read()

            originalFilePath = f + originalFileSuffix
            versionedOriginalFilePath = defineNextVersionedFilename(originalFilePath)

            with open(versionedOriginalFilePath, "w+") as fhO:
                fhO.write(fcontent)

            for k in replaceMap:
                # Make replacement step here. Modifies fcontent.
                fcontent = fcontent.replace(k, replaceMap[k])
                appendLog ("INFO", "Replacing %s -> %s" % ( k, replaceMap[k]))

            modifiedFilePath = f + replacedFileSuffix
            with open(modifiedFilePath, "w+") as fhM:
                fhM.write(fcontent)

        return (True)
    else:
        print("No replacement activites were performed.")
        return (False)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        replaceFileList = sys.argv[1]
        replaceStringList = sys.argv[2]
    appendLog("INFO", "Starting replaceInFiles session. replaceFileList: %s, replaceStringList: %s" % (replaceFileList, replaceStringList))
    fileList = parseFilePathFile(replaceFileList)
    appendLog("INFO", "%s" % (fileList))
    replaceExpressions = parseReplaceExpressions(replaceStringList)
    appendLog("INFO", "%s" % (replaceExpressions))
    replaceInFiles(fileList, replaceExpressions)
