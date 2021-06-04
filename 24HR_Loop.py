from distribution import Execute
import subprocess, time
from datetime import datetime, timedelta
import sys


if len(sys.argv) == 2:

    try:

        filename = sys.argv[1]

        while True:

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
            MEMOS = config[3]
            NEXT_TIME = config[4]
            if len(NEXT_TIME[0]) < 12:
                NEXT_TIME[0]+='0'
            print(NEXT_TIME)

            test = 1/len(TOKENS)
            test = 1/len(EXCEPTIONS)
            test = POT[0].split(":")
            test = [float(test[0]),test[1],test[2],test[3],test[4]]
            test = 1/len(MEMOS)
            del test


            next_time = NEXT_TIME[0]
            now = time.strftime("%Y%m%d%H%M")
            next_time_dt = datetime.strptime(next_time, '%Y%m%d%H%M')
            now_dt = datetime.strptime(now, '%Y%m%d%H%M')
            print("Next "+POT[0].split(":")[1]+" distribution to occur at "+str(next_time_dt)+" \nand time is "+str(now_dt))
            while float(next_time) > float(now):
                time_delta = (next_time_dt -now_dt)
                total_seconds = time_delta.total_seconds()
                minutes = total_seconds/60
                print(POT[0].split(":")[0]+" "+POT[0].split(":")[1]+" to distribute in "+str(minutes)+" minutes \nSleeping 30 minutes")
                time.sleep(1800)
                now = time.strftime("%Y%m%d%H%M")
                now_dt = datetime.strptime(now, '%Y%m%d%H%M')
            Execute.reward_holders(TOKENS,EXCEPTIONS,MEMOS,POT)
            new_next_time_dt = next_time_dt + timedelta(days=1)
            new_next_time_dt = new_next_time_dt.strftime('%Y%m%d%H%M')
            r_file = open(filename, "r")
            read_lines = r_file.readlines()
            r_file.close()
            for i in range(len(read_lines)):
                if next_time in read_lines[i]:
                    read_lines[i] = new_next_time_dt
            w_file = open(filename, "w")
            write_lines = w_file.writelines(read_lines)
            w_file.close()
            print("done, sleeping 3 hours")
            time.sleep(10800)
    except:
        print("Please check the docs \nand review input format.\n")
else:
    print("Please check the docs \nand review input format.\n")
