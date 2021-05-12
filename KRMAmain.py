from OurAssets import KRMA
from OurWork import Action
import subprocess
import time
import pandas as pd
import time
pd.set_option('display.max_colwidth', None)  # or 199'

with open("aboveheaven.txt") as infile:
    for line in infile:
        line = line.split(" ")
        if len(line[0]) > 10:
            sender = line[0]
        else:
            asset = [line[0],line[1][:-1]]

with open("KRMApot.txt") as infile:
    for line in infile:
        pot = float(line[:-1])


for i in range(3):
    cur_data,cur_dict = Action.get_holders(KRMA.collectables,pub=True,exceptions=KRMA.exceptions)
    members = Action.get_members(cur_data)
    holders_totals, percent_stakes = Action.get_totals(KRMA.collectables,cur_data,cur_dict,members)
    sendpot = Action.get_sendpot(pot,percent_stakes)
    print(" ")
    print("\t Totals ")
    df = pd.DataFrame(holders_totals)
    df.columns = df.iloc[0]
    df = df[1:]
    print(df)
    print(" ")
    print(" ")
    print("\t Totals by % ")
    df = pd.DataFrame(percent_stakes)
    df.columns = df.iloc[0]
    df = df[1:]
    print(df)
    print(" ")
    print(i)
    print(" ")
    print("\t Totals to send")
    df = pd.DataFrame(sendpot)
    print(df)
    print(" ")
    print(i)
    Action.send_payments(sendpot,sender,KRMA.earnable,'aboveheaven.txt',public=True)

    now = time.strftime("%Y%m%d%H%M")
    curday = now[-6:-4]
    curmin = now[-2:]

    cmd1 = ['./push_date.sh']
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p1.wait()

    with open('OurTime.txt') as inputfile:
        for line in inputfile:
            timed_day = line[-7:-5]
            timed_min = line[-3:-1]

    while curday == timed_day:
        time.sleep(10)
        print("Zzzzz")
        now = time.strftime("%Y%m%d%H%M")
        curday = now[-6:-4]
        curmin = now[-2:]
