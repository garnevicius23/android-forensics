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

def matching_string(x,y):
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

def calculate_words(messages_list):
    words_by_thread = {}
    all_words = {}

    for message in messages_list:

        if message[1] not in words_by_thread.keys():
            words_by_thread[message[1]] = {}

        for text in message[4].lower().split(" "):
            if len(words_by_thread[message[1]].keys()) == 0:
                words_by_thread[message[1]][text] = 1

            for key in list(words_by_thread[message[1]].keys()):
                if len(matching_string(text, key)) > 3:
                #if text in words_by_thread[message[1]].keys():
                    words_by_thread[message[1]][key] += 1
                else:
                    words_by_thread[message[1]][text] = 1
            
            if len(all_words) == 0:
                all_words[text] = 1

            for key in list(all_words.keys()):
                if len(matching_string(key, text)) > 4:
                    all_words[key] += 1
                    break;
                else:
                    all_words[text] = 1

    print(words_by_thread)
    print(len(all_words.keys()))
    print(len(matching_string("uogienes.", "uogiene")) > 3)

grant_root_permissions()
query = DataExtrator()

calculate_words(query.get_sms_list())

# _id[0], thread_id[1] , address[2], date[3], body[4], type[5]
# for row in query.get_sms_list():
#     print("id: ", row[0])
#     print("thread_id: ", row[1])
#     print("address: ", row[2])
#     print("date: ", row[3])
#     print("body: ", row[4])
#     print("type: ", row[5])
#     print("--------------")