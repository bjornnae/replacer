# replacer
Python utilities for batch find and replace functionality

Use for migration projects with many (more than 10) configuration files.

The setup is done by changing standard configuration files found in the folder conf. These are:

conf/replaceInFiles.txt
A list of paths to files that are to be worked upon by the replacement script.

conf/replaceCandidateRegexps.txt
A list of regexps pointing to strings that shall be replaced.

conf/replaceMap.txt
A map with replacements to be made where every line is in the form
<originalString> -> <targetString>
Replacement will be carried out from top to bottom, thus take care to arrange replacement instructions properly (typically it is a good approach to sort replacement instructions with longest originalString first and make sure that no targetString is found in a subsequent originalString in order to prevent unexpected output).




##

1. Configure your search and replace settings in the configuration files.
2. Run the identifyCandidates.py script. This will show you what the find part of the script will identify and print a list with [<fileName>:<lineNo>, [ found, values, matching, regexps]]
3.
