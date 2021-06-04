from distribution import Execute
import subprocess, time
from datetime import datetime, timedelta
import sys

if len(sys.argv) == 5:

    # try:
    filename = sys.argv[1]
    multiplier = sys.argv[2]
    amount = sys.argv[3]
    message = sys.argv[4]

    good = False
    try:
        float(amount)
        float(multiplier)
        if len(message) <= 28:
            good = True
    except:
        pass

    if good:

        config = []
        with open(filename) as infile:
            for line in infile:
                if "TOKENS" in line:
                    config.append([])
                elif "EXCEPTIONS" in line:
                    config.append([])
                elif "POT" in line:
                    config.append([])
                elif "MEMOS" in line:
                    config.append([])
                elif "NEXT_TIME" in line:
                    config.append([])
                else:
                    config[len(config)-1].append(line[:-1])
        infile.close()

        TOKENS = config[0]
        EXCEPTIONS = config[1]
        POT = config[2]
        MEMOS = [message]

        test = 1/len(TOKENS)
        test = 1/len(EXCEPTIONS)
        test = POT[0].split(":")
        test = [float(test[0]),test[1],test[2],test[3],test[4]]
        test = 1/len(MEMOS)
        del test

        if (float(multiplier) > 0):
            Execute.reward_holders(TOKENS,EXCEPTIONS,MEMOS,POT,MULT=float(multiplier))
        else:
            Execute.reward_holders(TOKENS,EXCEPTIONS,MEMOS,POT,FIXED_NUM=float(amount))
        print("done")
    # except:
    #     print("Please check the docs \nand review input format.\n")
else:
    print("You must enter 4 inputs: \ntext file, multiplier(or 0), fixed amount(or 0), and memo")
