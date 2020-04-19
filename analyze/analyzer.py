import os
import sys
import sqlite3

# File for research purposes

def grant_root_permissions():
    euid = os.geteuid()
    if euid != 0:
        print ("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

    print ('Running. Your euid is', euid)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def get_dbfile_sturcture(db_file):

     conn = create_connection(db_file)
     
     cur = conn.cursor()
     cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

     rows = cur.fetchall()

     for row in rows:
         print(row)

def get_sms_content():
    
     conn = create_connection("/mnt/loop0p23/user_de/0/com.android.providers.telephony/databases/mmssms.db")
     
     cur = conn.cursor()
     cur.execute("select * from sms")

     rows = cur.fetchall()

     #for row in rows:
         #print(row)

grant_root_permissions()

#get_sms_content()

for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
    for f in filenames:
        if "contacts" in os.path.join(dirpath, f):
            print('FILE :', f)
            #get_dbfile_sturcture(os.path.join(dirpath, f))
            
    # for d in dirnames:
    #     if "telephony" in os.path.join(dirpath, d):
    #         print('DIRECTORY :', os.path.join(dirpath, d))
    #         print('FILE :', os.path.join(dirpath, f))

