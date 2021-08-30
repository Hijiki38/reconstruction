import sys
import os
import FBP
import ART



if __name__ == '__main__':

    print("### Reconstruction ###")

    args = sys.argv
    mode = 0

    if len(args) < 2:
        inpath = "."
    else:
        inpath = args[1]
    while True:
        mode = input("Operation mode(0:FBP, 1:ART, 2:IR)")
        if int(mode) == 0 or int(mode) == 1 or int(mode) == 2:
            break
        else:
            print("error: invalid value")
    if int(mode) == 0:
        print("activate FBP...")
        FBP.FBPrec(inpath)
    elif int(mode) == 1:
        #print("activate ART...")
        print("ART is currently unavailable.")
        #ART.ARTrec(inpath)
