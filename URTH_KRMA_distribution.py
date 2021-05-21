from OurAssets import URTH
from OurAssets import KRMA
from OurWork import Action
from pandas import DataFrame as DF
from pandas import set_option
import time
from random import randint as rand
set_option('display.max_colwidth', None)

class Sender:

    def reward_holders():
        print("rewarding holders...")
        COLLECTABLES = [URTH.collectables,KRMA.collectables]

        exception_files = [URTH.exceptions,KRMA.exceptions]
        EXCEPTIONS = []
        for f in exception_files:
            with open(f) as infile:
                exceptiones = []
                for line in infile:
                    line = line.split("\n")
                    exceptiones.append(line[0])
                EXCEPTIONS.append(exceptiones)
                infile.close()

        memo_files = ["URTH_memos.txt","KRMA_memos.txt"]
        MEMOS = []
        for m in memo_files:
            with open(m) as infile:
                memorandums = []
                for line in infile:
                    line = line.split("\n")
                    memorandums.append(line[0])
                MEMOS.append(memorandums)
                infile.close()

        FILENAMES = [URTH.filename,KRMA.filename]

        pot_files = ["URTHpot.txt","KRMApot.txt"]
        POTS = []
        for p in pot_files:
            with open(p) as infile:
                for line in infile:
                    POTS.append(float(line.split("\n")[0]))
                infile.close()

        #loop through both asset distributions
        for i in range(2):

            cur_data,cur_dict = Action.get_holders(COLLECTABLES[i],EXCEPTIONS[i],public=True)
            members = Action.get_members(cur_data)
            holders_totals, percent_stakes = Action.get_totals(COLLECTABLES[i],cur_data,cur_dict,members)
            sendpot = Action.get_sendpot(POTS[i],percent_stakes)
            Receipt_String = ''
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
            index = rand(0,len(MEMOS[i])-1)
            receipt = Action.send_payments(sendpot,FILENAMES[i],MEMOS[i][index],public=True)
            Receipt_String += receipt

            # log transaction data
            receipt_file = "Receipts/"+time.strftime("%Y%m%d%H%M")+".txt"
            log = open(receipt_file,'a')
            log.write(Receipt_String)
            log.close()
            del Receipt_String, index
