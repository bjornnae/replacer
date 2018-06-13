#!/bin/env python

"""
Rollback activity to be used after replace activity

1) In the file conf/replaceInFiles.txt, comment out files that shall not be subjected to rollback.
2) run this script.

The script will look for the last previous version of a file by looking for filenames with a numeric extension (such as e.g. conf.xml has three previous versions, the last one being named conf.xml.3).
The previous version of the file will be used to overwrite the last version of the file.
The rolled back file will have the same modification timestamp as the previous version.

Note that as previous version files get rolled back they vanish from the history, thus you cannot undo a rollback (unless no configuration files have been changed.).

Subsequent calls to the rollback script will result in rolling back one version at a time.

When no more previous version files exist further calls for rollback will be denied.

"""


import gdeserializer
import os
import shutil
import replacer
import uuid

replaceStringList = replacer.replaceStringList
replaceFileList = replacer.replaceFileList
sid  = uuid.uuid1()

replacer.appendLog("INFO", "begin rollback#%s" % sid)
for f in gdeserializer.parseListFromFile(replaceFileList):
    latestPreviousVersion = replacer.defineLastVersionedFilename(f, f)
    if latestPreviousVersion == f:
        replacer.appendLog("INFO", "rollback#%s : No previous versions of file '%s' found. Will not do anything." % (sid, f))
        # Do nothing more for this file.
        pass
    else:
        # Do replace.
        shutil.move(latestPreviousVersion, f)
	replacer.appendLog("INFO", "rollback#%s : Moved %s into %s." % (sid, latestPreviousVersion, f))
replacer.appendLog("INFO", "end rollback#%s" % sid)