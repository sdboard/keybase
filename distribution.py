# from OurWork import Action
from Horizon_InterfaceSDB import Functions
from pandas import DataFrame as DF
from pandas import set_option
import time
from random import randint as rand
set_option('display.max_colwidth', None)

class Execute:

    def reward_holders(TOKENS,EXCEPTIONS,MEMOS,POT,PUB=False,MULT=0,FIXED_NUM=0):
        print("rewarding holders...")
        COLLECTABLES = []
        for t in TOKENS:
            COLLECTABLES.append([])
            for x in t.split(":"):
                COLLECTABLES[len(COLLECTABLES)-1].append(x)

        EXCEPT = []
        for e in EXCEPTIONS:
            EXCEPT.append(e)

        MEMO = MEMOS[rand(0,len(MEMOS)-1)]

        if not (MULT or FIXED_NUM):
            print(True)
        elif MULT:
            print("MULTIPLIER")
        else:
            print("FIXED_NUM")


        holders_totals, percent_stakes = Functions.get_percent_holders(COLLECTABLES,EXCEPT,public=PUB)
        Receipt_String = ''
        Receipt_String += "\n\t Totals "
        df = DF(holders_totals)
        Receipt_String += df.to_string()
        Receipt_String += "\n\n\t Totals by % "
        df = DF(percent_stakes)
        Receipt_String += df.to_string()
        Receipt_String += '\n\n\t Sending ..."'
        if not (MULT or FIXED_NUM):
            sendpot, receipt = Functions.send_payments(percent_stakes,POT,MEMO,public=PUB)
        elif MULT:
            sendpot, receipt = Functions.send_payments(holders_totals,POT,MEMO,public=PUB,multiplier=MULT)
        else:
            sendpot, receipt = Functions.send_payments(percent_stakes,POT,MEMO,public=PUB,fixed_amount=FIXED_NUM)
        df = DF(sendpot)
        Receipt_String += df.to_string()
        Receipt_String += receipt

        # log transaction data
        receipt_file = "Receipts/" + time.strftime("%Y%m%d%H%M")+ ".txt"
        log = open(receipt_file,'w')
        log.write(Receipt_String)
        log.close()


    def Trade():
        print("converting donated currencies")
        WISHING_WELLS = [TEST_URTH.wells,TEST_URTH.wells]
        log = ""
        for i in range(2):
            for well in WISHING_WELLS[i]:
                balance = Action.get_balance(well[1])
                if balance > 2:
                    print("here")
                    # Action.convert_to_USDC(well[1],TEST_URTH.filename,(balance-2))
                    Action.convert_to_USDC(well[1],TEST_URTH.filename,'100')
                    # log += "\n" + well[0] + " has collected " + balance
                # else: # log += "\n No appreciable change in "+well[0]
        # log transaction data
        # transaction_file = "TEST_Receipts/" + time.strftime("%Y%m%d%H%M")+ ".txt"
        # logger = open(transaction_file,'a')
        # logger.write(log)
        # logger.close()
        #
