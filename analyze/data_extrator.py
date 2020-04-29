import os, sys
import sqlite3

class DataExtrator:

    def create_connection(self, db_file):
        conn = None

        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        
        return conn


    # "Man atrodo" was deleted
    def get_sms_list(self):
        for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
            for f in filenames:
                if f == "mmssms.db":
                    print('FILE :', os.path.join(dirpath, f))
                    conn = self.create_connection(os.path.join(dirpath, f))
                    
                    curr = conn.cursor()
                    curr.execute("select _id, thread_id, address, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, body, case when type = 2 then 'sent' when type = 1 then 'received' end from sms order by thread_id, _id")
                    result = list(curr)

                    return result

    # TODO: check how actually calls is displayed
    def get_call_hisotry(self):
        for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
            for f in filenames:
                if f == "calllog.db":
                    print('FILE :', os.path.join(dirpath, f))
                    conn = self.create_connection(os.path.join(dirpath, f))
     
                    curr = conn.cursor()
                    curr.execute("select _id, name, number, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, case when type = 2 then 'outgoing' when type = 1 then 'incoming' end, (duration/60) duration  from calls where duration > 0")

                    return curr.fetchall()