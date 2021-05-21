from URTH_KRMA_distribution import Sender
import subprocess, time
from datetime import datetime, timedelta

while True:
    with open("Next_Time.txt") as infile:
        for line in infile:
            next_time = line.split("\n")[0]
    now = time.strftime("%Y%m%d%H%M")
    next_time_dt = datetime.strptime(next_time, '%Y%m%d%H%M')
    now_dt = datetime.strptime(now, '%Y%m%d%H%M')
    print("next distribution to occur at "+str(next_time_dt)+" and time is "+str(now_dt))
    while float(next_time) > float(now):
        print("wating 30 mins..")
        time.sleep(1800)
        now = time.strftime("%Y%m%d%H%M")

    Sender.reward_holders()
    # note next time
    next_time_dt += timedelta(days=1)
    next_time_dt = next_time_dt.strftime('%Y%m%d%H%M')
    next_file = open("Next_Time.txt",'w')
    next_file.write(next_time_dt)
    next_file.close()

    print("done, sleeping 1 hour")
    time.sleep(3600) # wait 1 hour
