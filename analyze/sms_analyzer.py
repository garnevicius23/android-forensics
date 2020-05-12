import os, sys
from data_extrator import DataExtrator

"""
Class to form data to later display in report.
"""

class MessagesAnalyzer():
    def __init__(self):
        self.all_words = {}
        self.words_by_thread = {}
        self.sms_statistics = {}
        self.calls_statistics = {}

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

            if message[2][-8:] not in self.words_by_thread.keys():
                self.words_by_thread[message[2][-8:]] = {}

            for text in message[4].lower().split(" "):

                # # Collect how much the same word was repeated through in each chat
                if len(self.words_by_thread[message[2][-8:]].keys()) == 0:
                    self.words_by_thread[message[2][-8:]][text] = 1
                else: 
                    if self.check_for_existing_thread(text, message[2][-8:]) == 0:
                        self.words_by_thread[message[2][-8:]][text] = 1

                
                # Collect how much the same word was repeated through all chats
                if len(self.all_words) == 0:
                    self.all_words[text] = 1
                else:
                    if self.check_for_existing(text) == 0 and not text == "":
                        self.all_words[text] = 1
                    
        self.all_words = sorted(self.all_words.items(), key=lambda x: x[1], reverse=True)
        #print(self.all_words)
        #print(len(self.all_words))

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

    def analyze_sms_statistics(self, sms_statistics_list):
        for row in sms_statistics_list:
            if row[2][-8:] not in self.sms_statistics.keys():
                # temporary list to store statistic data
                # idx 0 - name, idx 1 - incoming sms, idx 2 - outgoing sms, idx 3 - total
                if row[1] is None:
                    self.sms_statistics[row[2][-8:]] = ['No Name' ,0, 0, 0] 
                else:
                    self.sms_statistics[row[2][-8:]] = [row[1] ,0, 0, 0]
            
            self.sms_statistics[row[2][-8:]][3] += 1
            if row[3] == 'incoming':
                self.sms_statistics[row[2][-8:]][1] += 1
            elif row[3] == 'outgoing':
                self.sms_statistics[row[2][-8:]][2] += 1

    def analyze_calls_statistics(self, calls_statistics_list):
        for row in calls_statistics_list:
            if row[2][-8:] not in self.calls_statistics.keys():
                # temporary list to store statistic data
                # idx 0 - name, idx 1 - incoming call, idx 2 - outgoing call, idx 3 - missed, idx 4 -total
                if row[1] is None:
                    self.calls_statistics[row[2][-8:]] = ['No Name' ,0, 0, 0, 0]
                else:
                    self.calls_statistics[row[2][-8:]] = [row[1] ,0, 0, 0,0]
                
            self.calls_statistics[row[2][-8:]][4] += 1
            if row[3] == 'incoming':
                self.calls_statistics[row[2][-8:]][1] += 1
            elif row[3] == 'outgoing':
                self.calls_statistics[row[2][-8:]][2] += 1
            elif row[3] == 'missed':
                self.calls_statistics[row[2][-8:]][3] += 1

