from OurAssets import URTH
from OurWork import Action
import pandas as pd
import time
pd.set_option('display.max_colwidth', None)  # or 199
pot = 10
curtime = time.time()
for i in range(2):
    cur_data,cur_dict = Action.get_holders(URTH.collectables,pub=True,exceptions=URTH.exceptions)
    members = Action.get_members(cur_data)
    holders_totals, percent_stakes = Action.get_totals(URTH.collectables,cur_data,cur_dict,members)
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
    Action.send_payments(sendpot,URTH.earnable[1],URTH.earnable)
    curtime = time.time()
    while time.time() - curtime < 6:
        time.sleep(5)
