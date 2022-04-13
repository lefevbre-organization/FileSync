import logging
import time
import sys
import glob
import json
import datetime
# import test.utils as utils
# import test.queuemanager as queuemanager
import settings

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from schedule import every, repeat, run_pending

## logging configuration 
logging.basicConfig(filename='monitor.log', encoding='utf-8',level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

## settigs 
settings.Settings.init() # Call only once

print ("PROCESSED_FILES ------ " + settings.PROCESSED_FILES) 
print ("ERROR_FILES ---------- " + settings.ERROR_FILES) 
print ("DIRECTORY_TO_WATCH --- " + settings.DIRECTORY_TO_WATCH) 
print ("LOGGING_LEVEL -------- " + settings.LOGGING_LEVEL) 
    
# FileUtils = utils.Utils()
# FileUtils.move("file.log")
# print('utils_move_passed')
    
# QueueProcess = queuemanager.Queue()
# QueueProcess.main()
# print('queuemanager_main_passed')

## var to customize
##path_to_rclone_log_folder = r'LogRsync\*'
path_to_rclone_log_folder = settings.DIRECTORY_TO_WATCH + "\*"

## all possible action of rclone  
possible_action_rclone= ['Logname', 'stats', 'Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']
    
## start main process
def StartProcess ():
    ## get all log files of rclone_log_folder
    for logname in glob.glob(path_to_rclone_log_folder):
        print("\n\n\n++++++++ PROCESING LOG " + logname + "+++++++++++++")
        with open(logname,errors='ignore') as f:  # errors='ignore' : when strange character in log -then ignore
            content = f.readlines()
            list_of_actions_from_log = [x.strip() for x in content]

        ## read log and store each line in 
        datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
        # print(f"{datetime.datetime.now():%Y/%m/%d}")
        datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
        print("\n+++++++++++++ All actions +++++++++++++\n")
        select_actions_based_on_condition(datetime_beginning_of_time, logname, list_of_actions_from_log)
        
## Parse Logs and insert into a object
def select_actions_based_on_condition(datetime_condition, logname,  list_of_actions_from_log):

	## dico to save logs actions
	# create a dico log_actions
	# each key of log_actions is an item from possible_action_rclone
	# each value is an empty list, which would be used to store the action from rclone log
	log_actions ={key:[] for key in possible_action_rclone}  
	
	##loop trough log 
	for action_from_log in list_of_actions_from_log:
		
		key_found= False  # if key  found will be set to True

		for key, value in log_actions.items():	
			
			#check data type with type() method
			#convert string to json object
			msg_json_object = json.loads(action_from_log)

			#if key in Logname:
			if 'Logname' in key:				
				if len(log_actions[key]) == 0:
					log_actions[key].append(logname)


            #if key in stats:
			if 'stats' in key:				
				if 'stats' in msg_json_object:
					log_actions[key].append(action_from_log)
            #if key in action_from_log:
			if key in msg_json_object["msg"]:
				log_actions[key].append(action_from_log)
				key_found = True
		if key_found == False:
			log_actions['Others'].append(action_from_log)


	display_dico(log_actions) 	

## print logs object 
def display_dico(log_actions):
	
	empty_keys=[]  # if key empty, don't display it
	for key, value in log_actions.items():
		if len(value) != 0:
			print('\n')
			print('*******' + key+'*******')
			print('number of files: ', len(value))
			print(('\n').join(value))
		else:
			empty_keys.append(key)
	#print("Actions not done:" + (', ').join(empty_keys))

## main class
class Scheduler: 
        
    def __init__(self):
        self.observer = Observer()


        while True:
            run_pending()
            time.sleep(1)

    ## start the timer
    @repeat(every(10).seconds)
    def job():
        print("start scheduled job")        
        logging.info("Start Job")
        StartProcess()


if __name__ == '__main__':
    w = Scheduler()
    

