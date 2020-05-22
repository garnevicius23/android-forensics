import os, sys
import sqlite3

"""
Class to perform different queries to database to retrieve data for
different calculations.
"""

class DataExtrator:

    def __init__(self, working_dir):
        self.working_dir = working_dir

    def create_connection(self, db_file):
        conn = None

        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        
        return conn


    def get_sms_list(self):
        if os.path.exists(self.working_dir + '/telephony/mmssms.db'):
            print('FILE :', self.working_dir + '/telephony/mmssms.db')
            conn = self.create_connection(self.working_dir + '/telephony/mmssms.db')
                    
            curr = conn.cursor()
            curr.execute("select _id, thread_id, address, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, body, case when type = 2 then 'sent' when type = 1 then 'received' end from sms order by thread_id, _id")
            result = list(curr)

            return result
        else:
            for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
                for f in filenames:
                    if f == "mmssms.db":
                        print('FILE :', os.path.join(dirpath, f))
                        conn = self.create_connection(os.path.join(dirpath, f))
                        
                        curr = conn.cursor()
                        curr.execute("select _id, thread_id, address, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, body, case when type = 2 then 'sent' when type = 1 then 'received' end from sms order by thread_id, _id")
                        result = list(curr)

                        return result

    def get_call_hisotry(self):
        if os.path.exists(self.working_dir + '/telephony/calllog.db'):
            print('FILE :', self.working_dir + '/telephony/calllog.db')
            conn = self.create_connection(self.working_dir + '/telephony/calllog.db')
                    
            curr = conn.cursor()
            curr.execute("select _id, name, number, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, case when type = 2 then 'outgoing' when type = 1 then 'incoming' when type = 3 then 'missed' else type end, duration  from calls where duration > 0")

            return curr.fetchall()
        else:
            for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
                for f in filenames:
                    if f == "calllog.db":
                        print('FILE :', os.path.join(dirpath, f))
                        conn = self.create_connection(os.path.join(dirpath, f))
        
                        curr = conn.cursor()
                        curr.execute("select _id, name, number, strftime('%Y-%m-%d %H:%M:%S', date/1000, 'unixepoch') date, case when type = 2 then 'outgoing' when type = 1 then 'incoming' when type = 3 then 'missed' else type end, duration  from calls where duration > 0")

                        return curr.fetchall()

    def get_sms_statistics(self):
        if os.path.exists(self.working_dir + '/telephony/calllog.db'):
            print('FILE :', self.working_dir + '/telephony/calllog.db')
            conn = self.create_connection(self.working_dir + '/telephony/calllog.db')
                    
            curr = conn.cursor()
            curr.execute("select _id, name, number,  case when type = 2 then 'outgoing' when type = 1 then 'incoming' else type end  from calls where messageid is not null;")

            return curr.fetchall()
        else:
            for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
                for f in filenames:
                    if f == "calllog.db":
                        print('FILE :', os.path.join(dirpath, f))
                        conn = self.create_connection(os.path.join(dirpath, f))
        
                        curr = conn.cursor()
                        curr.execute("select _id, name, number,  case when type = 2 then 'outgoing' when type = 1 then 'incoming' else type end  from calls where messageid is not null;")

                        return curr.fetchall()

    def get_calls_statistics(self):
        if os.path.exists(self.working_dir + '/telephony/calllog.db'):
            print('FILE :', self.working_dir + '/telephony/calllog.db')
            conn = self.create_connection(self.working_dir + '/telephony/calllog.db')
                    
            curr = conn.cursor()
            curr.execute("select _id, name, number,  case when type = 2 then 'outgoing' when type = 1 then 'incoming' when type = 3 then 'missed' else type end  from calls where messageid is null;")

            return curr.fetchall()
        else:
            for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
                for f in filenames:
                    if f == "calllog.db":
                        print('FILE :', os.path.join(dirpath, f))
                        conn = self.create_connection(os.path.join(dirpath, f))
        
                        curr = conn.cursor()
                        curr.execute("select _id, name, number,  case when type = 2 then 'outgoing' when type = 1 then 'incoming' when type = 3 then 'missed' else type end  from calls where messageid is null;")

                        return curr.fetchall()
