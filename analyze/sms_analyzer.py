import os, sys
from data_extrator import DataExtrator

def grant_root_permissions():
    euid = os.geteuid()
    if euid != 0:
        print ("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

    print ('Running. Your euid is', euid)

grant_root_permissions()
query = DataExtrator()

# _id[0], thread_id[1] , address[2], date[3], body[4], type[5]
for row in query.get_sms_list():
    print("id: ", row[0])
    print("thread_id: ", row[1])
    print("address: ", row[2])
    print("date: ", row[3])
    print("body: ", row[4])
    print("type: ", row[5])
    print("--------------")