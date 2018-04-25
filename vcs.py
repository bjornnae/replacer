#!/bin/env/python
"""
VCS - A very simple version control system.

Versions of files are stored as full copies and indexed by content hash.

Filenames of versions are suffixed with revision number.
If the file under version is called testFile.txt, previous revisions might be called
testFile.txt.1
testFile.txt.2

The revision number reflects a transaction line in the __vcsTransactionFileName
which is the metadata text file associating filename with checksum and timestamp.


"""

import shutil
import md5


__vcsFolder = ".vcs"
__vcsTransactionFileName = "%s/vcs.dat" % __vcsFolder
__vcsLogFileName = "%s/vcs.log" % __vcsFolder
__vcsRecordDelimiter = ";"
__vcsPathDelimiter = "/"


def checksum(filePath):
    m = md5.new()
    with open(filePath) as fh:
        m.update(fh.read())
    return(m.digest())

def countFileLines(filePath):
    linesC = 0
    for line in open(filePath):
        linesC += 1
    return linesC


def parseTransactionEntry(transactionEntryLine):
    splitted = transactionEntryLine.split(__vcsRecordDelimiter)
    return({"operation" : splitted[0], "fileName" : splitted[1], "checksum" : splitted[2], "timestamp" : splitted[3]})


def snapTransaction(command, filePath):
    timestamp = time.now()
    with open(filePath, "r") as fh:
        checksum = checksum(fh.read())
    return(command + __vcsRecordDelimiter + filePath + __vcsRecordDelimiter + checksum + __vcsRecordDelimiter + timestamp)


def transactionLogAppend(command, filePath):
    line = snapTransaction(command, filePath)
    with open(__vcsTransactionFileName, "a") as fh:
        fh.write(line)
    return(line)


def vcsExist(folderPath):
    files = os.listdir(folderPath)
    if __vcsFolder in files:
        return(True)
    else:
        return(False)


def vcsInit(folderPath):
    if vcsExist(folderPath):
        print("Vcs already exist, will not create.")
    else:
        os.mkdir(folderPath + "/" + __vcsFolder)
        with open(__vcsTransactionFileName, "w+") as fh:
            transactionLine = snapTransaction("init", __vcsTransactionFileName)
            fh.write(transactionLine)
    return(transactionLine)


def vcsStatus(filePath):
    pass


def vcsCommit(filePath):
    linesInTransactionFile = countFileLines(__vcsTransactionFileName)
    fn = filePath.split(__vcsPathDelimiter)[-1]
    storedFileName = fn + "." + linesInTransactionFile
    storedFilePath = __vcsFolder + __vcsPathDelimiter + storedFileName
    os.copy(filePath, storedFilePath)
    transactionLine = transactionLogAppend("commit", storedFilePath)
    return(transactionLine)


def vcsRollBack(filePath):
    pass


def vcsAdd(filePath):
    transactionLine = transactionLogAppend("add", filePath)
    return(transactionLine)


def vcsRemove():
    shutil.rmtree(__vcsFolder, ignore_errors=True)


if __name__ == "__main__":
    testDir = "./testfiles"
    testFile = testDir + "/testFile.txt"
    vcsInit(testDir)
    vcsAdd("testDir/testFile.txt")
    vcsCommit("testDir/testFile.txt")
