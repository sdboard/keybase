from OurAssets import URTH
from OurAssets import KRMA
from OurWork import Action
from pandas import DataFrame as DF
from pandas import set_option
import subprocess
import time
set_option('display.max_colwidth', None)

COLLECTABLES = [URTH.collectables,KRMA.collectables]
EXCEPTIONS = [URTH.exceptions,KRMA.exceptions]
FILENAMES = [URTH.filename,KRMA.filename]

with open("URTHpot.txt") as infile:
    for line in infile:
        URTHpot = float(line[:-1])

with open("KRMApot.txt") as infile:
    for line in infile:
        KRMApot = float(line[:-1])

POTS = [URTHpot,KRMApot]
'''
##############################################################################
      ######   Because yesterday's distribution had an error,   ######
      ######   I need to catch up with one URTH distribution    ######
##############################################################################
'''
cur_data,cur_dict = Action.get_holders(COLLECTABLES[0],EXCEPTIONS[0],public=True)
members = Action.get_members(cur_data)
holders_totals, percent_stakes = Action.get_totals(COLLECTABLES[0],cur_data,cur_dict,members)
sendpot = Action.get_sendpot(POTS[0],percent_stakes)
Receipt_String = '"'
Receipt_String += "\n\t Totals "
df = DF(holders_totals)
Receipt_String += df.to_string()
Receipt_String += "\n\n\t Totals by % "
df = DF(percent_stakes)
Receipt_String += df.to_string()
Receipt_String += "\n\n\t Totals to send"
df = DF(sendpot)
Receipt_String += df.to_string()
Receipt_String += '\n\n\t Sending ..."'
receipt = Action.send_payments(sendpot,FILENAMES[0],public=True)
Receipt_String += receipt
# log transaction data
receipt_file = "Receipts/"
receipt_file += time.strftime("%Y%m%d%H%M")
receipt_file += ".txt"
log = open(receipt_file,'a')
log.write(Receipt_String)
log.close()
'''
##############################################################################
              Delete above section for future runs
##############################################################################
'''
for i in range(3): # run for 3 days

    now = time.strftime("%Y%m%d%H%M")
    curday = now[-6:-4] # get current day of month

    cmd1 = ['./push_date.sh']
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p1.wait() # save current day of month to text file

    with open('OurTime.txt') as inputfile:
        for line in inputfile: # pull saved day of month
            timed_day = line[-7:-5]

    while curday == timed_day: # while we haven't changed days
        print("Zzzzz")
        time.sleep(10800) # wait 3 hours
        now = time.strftime("%Y%m%d%H%M")
        curday = now[-6:-4] # get current day

    #loop through both asset distributions
    for i in range(2):
        cur_data,cur_dict = Action.get_holders(COLLECTABLES[i],EXCEPTIONS[i],pub=True)
        members = Action.get_members(cur_data)
        holders_totals, percent_stakes = Action.get_totals(COLLECTABLES[i],cur_data,cur_dict,members)
        sendpot = Action.get_sendpot(POTS[i],percent_stakes)
        Receipt_String = '"'
        Receipt_String += "\n\t Totals "
        df = DF(holders_totals)
        Receipt_String += df.to_string()
        Receipt_String += "\n\n\t Totals by % "
        df = DF(percent_stakes)
        Receipt_String += df.to_string()
        Receipt_String += "\n\n\t Totals to send"
        df = DF(sendpot)
        Receipt_String += df.to_string()
        Receipt_String += '\n\n\t Sending ..."'
        receipt = Action.send_payments(sendpot,FILENAMES[i],public=True)
        Receipt_String += receipt

        # log transaction data
        receipt_file = "Receipts/"
        receipt_file += time.strftime("%Y%m%d%H%M")
        receipt_file += ".txt"
        log = open(receipt_file,'a')
        log.write(Receipt_String)
        log.close()
