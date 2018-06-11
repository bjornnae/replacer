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
import os
import shutil
import md5
import time


__vcsFolder = ".vcs"
__vcsTransactionFileName = "%s/vcs.dat" % __vcsFolder
__vcsLogFileName = "%s/vcs.log" % __vcsFolder
__vcsRecordDelimiter = ";"
__vcsPathDelimiter = "/"
__vcsLineDelimiter = "\n"


def calcChecksum(filePath):
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
    timestamp = time.time()
    checksum = calcChecksum(filePath)
    return(str(timestamp) +  __vcsRecordDelimiter + command + __vcsRecordDelimiter + filePath + __vcsRecordDelimiter + str(checksum))


def transactionLogAppend(vcsRoot, command, filePath):
    line = snapTransaction(command, filePath)
    with open(vcsRoot + __vcsPathDelimiter + __vcsTransactionFileName, "a") as fh:
        fh.write(line + __vcsLineDelimiter)
    return(line)


def vcsExist(vcsRoot):
    files = os.listdir(vcsRoot)
    if __vcsFolder in files:
        return(True)
    else:
        return(False)


def vcsInit(vcsRoot):
    if vcsExist(vcsRoot):
        print("Vcs already exist, will not create.")
    else:
        os.mkdir(vcsRoot + "/" + __vcsFolder)
        timestamp = time.time()
        command = "init"
        checksum = ""
        transactionLine =  str(timestamp) +  __vcsRecordDelimiter + command + __vcsRecordDelimiter + __vcsTransactionFileName + __vcsRecordDelimiter + str(checksum) + __vcsLineDelimiter
        with open(vcsRoot + __vcsPathDelimiter + __vcsTransactionFileName, "w+") as fh:
            fh.write(transactionLine)
        return(transactionLine)


def vcsStatus(vcsRoot):
    pass


def vcsCommit(vcsRoot, filePath):
    linesInTransactionFile = countFileLines(vcsRoot + __vcsPathDelimiter + __vcsTransactionFileName)
    fn = filePath.split(__vcsPathDelimiter)[-1]
    storedFileName = fn + "." + str(linesInTransactionFile)
    storedFilePath = vcsRoot + __vcsPathDelimiter + __vcsFolder + __vcsPathDelimiter + storedFileName
    shutil.copy(filePath, storedFilePath)
    transactionLine = transactionLogAppend(vcsRoot, "commit", storedFilePath)
    return(transactionLine)


def vcsRollBack(filePath):
    pass


def vcsAdd(vcsRoot, filePath):
    transactionLine = transactionLogAppend(vcsRoot, "add", filePath)
    return(transactionLine)


def vcsRemove():
    shutil.rmtree(vcsRoot + __vcsPathDelimiter + __vcsFolder, ignore_errors=True)


if __name__ == "__main__":
    vcsRoot = "./testfiles"
    testFile = vcsRoot + "/testFile.txt"
    vcsInit(vcsRoot)
    vcsAdd(vcsRoot,  vcsRoot +  "/testFile.txt")
    vcsCommit(vcsRoot, vcsRoot + "/testFile.txt")
