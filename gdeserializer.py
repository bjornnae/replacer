# Generic deserializer
import os
import re


_newlinesym = "\n"
_mapsepsym = " -> "


def parseListFromFile(filePath):
    with  open(filePath, "r") as fh:
        lines = fh.readlines()
    result = []
    for l in lines:
        if l[0] == "#":
            # The parser has encountered a comment line, do nothing:
            pass
        elif l[-1] == _newlinesym:
            result.append(l[0:-1])
        else:
            result.append(l)
    return(result)

def putListToFile(filePath, aList):
    with open(filePath, 'w+') as fh:
        fh.writelines(("%s" + _newlinesym) % l for l in aList)
    return(True)


def parseHashMapFromFile(filePath):
    with  open(filePath, "r") as fh:
        lines = fh.readlines()
    result = {}
    for l in lines:
        splitted = l.split(_mapsepsym)
        if l[0] == "#":
            # The parser has encountered a comment line, do nothing:
            pass
        elif l[0] == _newlinesym:
            # the line is empty, do nothing.
            pass
        elif splitted[-1][-1] == _newlinesym:
            try:
                result[splitted[0]] = splitted[1][0:-1]
            except IndexError:
                print("Input does not follow required format. Input is (%s)" % l)
        else:
            result[splitted[0]] = splitted[1]
    return(result)

def putHashMapToFile(filePath, aDict):
    lines = []
    for k, v in aDict.iteritems():
        lines.append(k + _mapsepsym + v + _newlinesym)

    with open(filePath, 'w+') as fh:
        fh.write("".join(lines))
    return(True)


def parseRegexpListFromFile(filePath):
    """ filePath is a list of regexps, verify that they are parsable. Return list of regexp strings (not compiled re.objects). """
    regexpList = parseListFromFile(filePath)
    for r in regexpList:
        try:
            re.compile(r) # This will throw an exception if not possible.
        except Exception as e:
            print("WARN: re: '%s' is not a good regexp!. (error was: %s)" % (r, e))
            regexpList = []
    return( regexpList )


if __name__ == "__main__":
    t1lst = ["A", "B", "C"]
    path1 = "./testFile.txt"
    putListToFile(path1, t1lst)
    t2lst = parseListFromFile(path1)
    try:
        assert(t1lst == t2lst)
        print("T1 PASS")
        os.remove(path1)
    except AssertionError:
        print("1> %s" % t1lst)
        print("2> %s" % t2lst)
        print("Leaving test file for post mortem analysis: %s" % path1)
        print("T1 FAIL")

    print("Test2: Dictionary input and output.")
    path2 = "./testfile2.txt"
    t3dict = {"a" : "b", "c" : "d"}
    putHashMapToFile(path2, t3dict)
    t4dict = parseHashMapFromFile(path2)
    try:
        assert(t3dict == t4dict)
        print("T2 PASS")
        os.remove(path2)
    except AssertionError:
        print("1> %s" % t3dict)
        print("2> %s" % t4dict)
        print("Leaving test file for post mortem analysis: %s" % path2)
        print("T2 FAIL")
