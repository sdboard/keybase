# from OurWork import Action
from Horizon_InterfaceSDB import Functions
from pandas import DataFrame as DF
from pandas import set_option
from random import randint as rand
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib

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

        holders_totals, percent_stakes = Functions.get_percent_holders(COLLECTABLES,EXCEPT,public=PUB)

        if not (MULT or FIXED_NUM):
            sendpot, receipt = Functions.send_payments(percent_stakes,POT,MEMO,public=PUB)
        elif MULT:
            sendpot, receipt = Functions.send_payments(holders_totals,POT,MEMO,public=PUB,multiplier=MULT)
        else:
            sendpot, receipt = Functions.send_payments(percent_stakes,POT,MEMO,public=PUB,fixed_amount=FIXED_NUM)

        Receipt_String = "\n\t Totals " + DF(holders_totals).to_string()
        Receipt_String += "\n\n\t Totals by % " + DF(percent_stakes).to_string()
        Receipt_String += '\n\n\t Sending ..."' + DF(sendpot).to_string() + receipt

        # log transaction data locally
        receipt_file = "Receipts/" + time.strftime("%Y%m%d%H%M")+ ".txt"
        log = open(receipt_file,'w')
        log.write(Receipt_String)
        log.close()

        return Receipt_String,receipt_file

    def check_dist_ballance(info,pub):
        pub_key = info.split(":")[3]
        code = info.split(":")[1]
        issuer = info.split(":")[2]
        return Functions.get_balance(pub_key,asset=[code,issuer],public=pub)

    def post_process(text):
        return text

    def broadcast_results(receipt,file,time,email,days_left=0):
        msg = MIMEMultipart()
        if days_left:
            subject = "William, only " + str(days_left) + " days balance remains!"
        else:
            subject = time + " distribution recap"
        msg['Subject'] = subject
        # msg.attach(MIMEText(post_process(receipt)))
        msg.attach(MIMEText("Recap attached"))
        attachment = open(file, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file)
        msg.attach(p)
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(email[0], email[3])
        text = msg.as_string()
        smtp.sendmail(email[0],[email[1],email[2]],text)
        smtp.quit()

    def auto_depositor():
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
