from distribution import Execute
import subprocess, time, sys, smtplib, ssl
from datetime import datetime, timedelta

def scan(filename):
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
            elif "EMAIL" in line:
                config.append([])
            elif "NEXT_TIME" in line:
                config.append([])
            else:
                config[len(config)-1].append(line[:-1])
    infile.close()
    if len(config[5][0]) < 12:
        config[5][0]+='0'
    return (config[0],config[1],config[2],config[3],config[4],config[5])

def test(TOKENS,EXCEPTIONS,POT,MEMOS):
    test = 1/len(TOKENS)
    test = 1/len(EXCEPTIONS)
    test = POT[0].split(":")
    test = [float(test[0]),test[1],test[2],test[3],test[4]]
    test = 1/len(MEMOS)
    del test

def increment_time(old_time_str,old_time,filename):
    new_time = old_time + timedelta(days=1)
    new_time = new_time.strftime('%Y%m%d%H%M')
    r_file = open(filename, "r")
    read_lines = r_file.readlines()
    r_file.close()
    for i in range(len(read_lines)):
        if old_time_str in read_lines[i]:
            read_lines[i] = new_time
    w_file = open(filename, "w")
    write_lines = w_file.writelines(read_lines)
    w_file.close()

def broadcast_results(receipt,time,email):
    context = ssl.create_default_context()
    port =  465
    message = "Subject: "+time+" transactions \n\n"+receipt
    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login("krma.backend@gmail.com",email[2])
        server.sendmail("krma.backend@gmail.com",[email[0],email[1]],message)

def get_time(next_str):
    now = time.strftime("%Y%m%d%H%M")
    next_time_dt = datetime.strptime(next_str, '%Y%m%d%H%M')
    now_dt = datetime.strptime(now, '%Y%m%d%H%M')
    return next_time_dt, now_dt, now

def main(filename):
    while True:
        TOKENS,EXCEPTIONS,POT,MEMOS,EMAIL,NEXT_TIME = scan(filename)
        next,now,now_str = get_time(NEXT_TIME[0])
        print("time is "+str(now)+" and "+POT[0].split(":")[0]+
            " "+POT[0].split(":")[1]+" to distribute at "+str(next))
        while float(NEXT_TIME[0]) > float(now_str):
            choice = min([3600,(next-now).total_seconds()])
            print("Sleeping "+str(choice/60)+" minutes...")
            time.sleep(choice)
            next,now,now_str = get_time(NEXT_TIME[0])
            print(POT[0].split(":")[0]+" "+POT[0].split(":")[1]+
                " to distribute in "+str((next-now).total_seconds()/60)+" minutes.")
        TOKENS,EXCEPTIONS,POT,MEMOS,EMAIL,NEXT_TIME = scan(filename)
        test(TOKENS,EXCEPTIONS,POT,MEMOS)
        receipt = Execute.reward_holders(TOKENS,EXCEPTIONS,MEMOS,POT,PUB=True)
        broadcast_results(receipt,NEXT_TIME[0],EMAIL)
        increment_time(NEXT_TIME[0],next,filename)

if len(sys.argv) == 2:
    try:
        filename = sys.argv[1]
        main(filename)
    except:
        print("Something went wrong")
else:
    print("Please check the docs \nand review input format.\n")
