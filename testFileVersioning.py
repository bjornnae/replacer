import replacer as r

import os.path

def test1():
    filename = "testfiles/conf1.dat"
    r1 = r.stripCounter(filename)
    print("r1:" + str(r1))
    assert ( r1 == ("testfiles/conf1.dat", 0) )
    r2 = r.stripCounter(r1[0]+ "." + str(r1[1]))
    print("r2:" + str(r2))
    assert ( r1 == ("testfiles/conf1.dat", 0) )


    nextfilename = r.defineNextVersionedFilename(filename)
    print("debug: nextfilename: %s" % nextfilename)

    with open(nextfilename, "w+") as fh0:
        fh0.write("Some file content.")

test1()
