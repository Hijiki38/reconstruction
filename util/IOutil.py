import glob

def ChooseFiles(condition):
        candidates = glob.glob(condition)
        for i in range(len(candidates)):
            print(str(i) + ": " + candidates[i])
        while True:
            tmp = input("Choose Input File:")
            if int(tmp) >= 0 and int(tmp) < len(candidates):
                infile = candidates[int(tmp)]
                break
            else:
                print("error: invalid value")
        return infile
