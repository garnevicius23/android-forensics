import os, sys
import shutil

def grant_root_permissions():
    euid = os.geteuid()
    if euid != 0:
        print ("Script not started as root. Running sudo..")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)

    print ('Running. Your euid is', euid)

def create_directories(path):
    for dir_name in ("/pictures", "/telephony"):
        os.mkdir(path + dir_name)
    

def copy_files(working_dir):
    print("hello?")
    for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
        for f in filenames:
            if f == "mmssms.db":
                src_file = os.path.join(dirpath, f)
                dest_path = working_dir + "/telephony"
                shutil.copy(src_file, dest_path)
            elif f == "calllog.db":
                src_file = os.path.join(dirpath, f)
                dest_path = working_dir + "/telephony"
                shutil.copy(src_file, dest_path)
                
grant_root_permissions()
create_directories(sys.argv[1])
copy_files(sys.argv[1])

#for (dirpath, dirnames, filenames) in os.walk('/mnt/'):
#            for f in filenames: