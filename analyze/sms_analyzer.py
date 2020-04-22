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

class MessagesAnalyzer():
    def __init__(self):
        self.all_words = {}
        self.words_by_thread = {}

    # Check how many characters in two words are matching
    def matching_string(self, x,y):
        match=''
        for i in range(0,len(x)):
            for j in range(0,len(y)):
                k=1
                # now applying while condition untill we find a substring match and length of substring is less than length of x and y
                while (i+k <= len(x) and j+k <= len(y) and x[i:i+k]==y[j:j+k]):
                    if len(match) <= len(x[i:i+k]):
                        match = x[i:i+k]
                    k=k+1
        return match  

    def calculate_words(self, messages_list):
        for message in messages_list:

            if message[1] not in self.words_by_thread.keys():
                self.words_by_thread[message[1]] = {}

            for text in message[4].lower().split(" "):

                # # Collect how much the same word was repeated through in each chat
                if len(self.words_by_thread[message[1]].keys()) == 0:
                    self.words_by_thread[message[1]][text] = 1
                else: 
                    if self.check_for_existing_thread(text, message[1]) == 0:
                        self.words_by_thread[message[1]][text] = 1

                
                # Collect how much the same word was repeated through all chats
                if len(self.all_words) == 0:
                    self.all_words[text] = 1
                else:
                    if self.check_for_existing(text) == 0 and not text == "":
                        self.all_words[text] = 1
                    
        self.all_words = sorted(self.all_words.items(), key=lambda x: x[1], reverse=True)
        print(self.all_words)
        print(len(self.all_words))

    def check_for_existing_thread(self, text, thread):
        for key in list(self.words_by_thread[thread].keys()):
            if len(self.matching_string(text, key)) > 5 or text == key:
                self.words_by_thread[thread][key] += 1
                return 1
        
        return 0


    def check_for_existing(self, text):
        for key in list(self.all_words.keys()):

            if (len(self.matching_string(key, text)) > 5 or text == key) and not text == "":
                self.all_words[key] += 1
                return 1
        
        return 0

                

grant_root_permissions()
query = DataExtrator()

sms = MessagesAnalyzer()
sms.calculate_words(query.get_sms_list())

# _id[0], thread_id[1] , address[2], date[3], body[4], type[5]
# for row in query.get_sms_list():
#     print("id: ", row[0])
#     print("thread_id: ", row[1])
#     print("address: ", row[2])
#     print("date: ", row[3])
#     print("body: ", row[4])
#     print("type: ", row[5])
#     print("--------------")