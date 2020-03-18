import sys
import time
import daemon

def count_up():
    count = 0
    while True:
        print(count)
        count += 1
        time.sleep(1)

dc = daemon.DaemonContext(stdout=sys.stdout)

with dc:
    count_up()
