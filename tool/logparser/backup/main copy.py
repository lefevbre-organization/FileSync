from asyncore import loop
import logging
import time
import glob
import json
import datetime
import queue
import threading
import requests
import settings
import parser
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
print ("QUEUE_TIME ----------- " + str(settings.QUEUE_TIME)) 
    
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
possible_action_rclone= ['Logname','stats','Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']
    
## start main process
def startprocess ():
    ## get all log files of rclone_log_folder
    inxforTrhead=0
    for logname in glob.glob(path_to_rclone_log_folder):
        inxforTrhead = inxforTrhead + 1
        print("\n\n\n++++++++ PROCESING LOG " + logname + "+++++++++++++")
        with open(logname,errors='ignore') as f:  # errors='ignore' : when strange character in log -then ignore
            content = f.readlines()
            list_of_actions_from_log = [x.strip() for x in content]

        ## read log and store each line in 
        datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
        # print(f"{datetime.datetime.now():%Y/%m/%d}")
        datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
        print("\n+++++++++++++ All actions +++++++++++++\n")
        log_actions = parser.select_actions_based_on_condition(datetime_beginning_of_time, logname, list_of_actions_from_log)
                
        q = queue.Queue()		
        worker = threading.Thread(target=main_queue, args=(q, inxforTrhead,log_actions), daemon=True)
        worker.start()
        q.put(logname)		
        q.join()
        
## Parse Logs and insert into a object
# def select_actions_based_on_condition(datetime_condition, logname,  list_of_actions_from_log):

# 	## dico to save logs actions
# 	# create a dico log_actions
# 	# each key of log_actions is an item from possible_action_rclone
# 	# each value is an empty list, which would be used to store the action from rclone log
# 	log_actions ={key:[] for key in possible_action_rclone}  

#     # log_actions['logname'].append(logname)
#     # log_actions['Stats'].append(logname)
    
    
# 	##loop trough log 
# 	for action_from_log in list_of_actions_from_log:
		
# 		key_found= False  # if key  found will be set to True

# 		for key, value in log_actions.items():	
			
# 			#check data type with type() method
# 			# #convert string to json object
# 			msg_json_object = json.loads(action_from_log)

# 			#if key in Logname:
# 			if 'Logname' in key:				
# 				if len(log_actions[key]) == 0:
# 					log_actions[key].append(logname)

#             #if key in stats:
# 			if 'stats' in key:				
# 				if 'stats' in action_from_log:
# 					log_actions[key].append(action_from_log)
# 					break

#             #if key in action_from_log:            
# 			if key in msg_json_object["msg"] :			
# 				log_actions[key].append(action_from_log)
# 				key_found = True
# 		if key_found == False:
# 			log_actions['Others'].append(action_from_log)

# 	return log_actions

## print logs object 
def process_dico(log_actions):
	
	empty_keys=[]  # if key empty, don't display it
	for key, value in log_actions.items():
		if len(value) != 0:	    
			print('\n')
			print('*******' + key+'*******')
			print('number of files: ', len(value))
			print(('\n').join(value))

			## process to call differents enpoinf depending of action type
			## excludig the "Other tags or "Logname""		
			if (key != "Others" and key != "Logname" and key != "stats"):
				api_method_parser(key,value)
            

		else:
			empty_keys.append(key)
	#print("Actions not done:" + (', ').join(empty_keys))

def main_queue(q, thread_no,log_actions ):
    while True:
        task = q.get()
        time.sleep(settings.QUEUE_TIME)
        print(f'Thread #{thread_no} is doing task #{task} in the main queue.')
        process_dico(log_actions)
        q.task_done()
        print(f'Thread #{thread_no} completed #{task} of the main queue.')

def api_queue(qApi, thread_no,log_action):
    while True:
        task = qApi.get()
        time.sleep(settings.QUEUE_TIME)
        print(f'Thread #{thread_no} is doing task #{task} in the api queue.')
        #select Swich method depending action
        api_method_deleted_async(log_action)
        
        qApi.task_done()
        print(f'Thread #{thread_no} completed #{task} of the api queue.')
        
def api_method_deleted_async(log_action):
    
    response = requests.post('https://httpbin.org/post', data = {'key':'value'})    
    if (response.status_code == 200):
        print("The request was a success!")
        # Code here will only run if the request is successful
    elif (response.status_code) == 404:
        print("Result not found!")
			# Code here will react to failed requests
    
def api_method_parser(key, actionCollection):
    qApi = queue.Queue()
    for i in actionCollection:        
        # print('APIDeleted') 

        json_object_msg = json.loads(i) 
        workerApi = threading.Thread(target=api_queue, args=(qApi, json_object_msg['object'], key), daemon=True)
        workerApi.start()
        qApi.put('api_action_ ' + key)		
        qApi.join()     
        


# def callEndPoint(condition, value):            
#     if condition == 'Deleted':
#         print('API - Deleted')        
#         APIDeleted(value)        
#     elif condition == 'Renamed':
#         APIDeleted(value)
#         print('API - Renamed')
#     elif condition == 'Copy':
#         APIDeleted(value)
#         print('API - Copy')
#     elif condition == 'Others':
#         print('others')
#     else:
#         return None
    
## main class
class Scheduler: 
        
    def __init__(self):
        startprocess()
        self.observer = Observer()


        while True:
            run_pending()
            time.sleep(1)

    ## start the timer
    @repeat(every(120).seconds)
    def job():
        print("start scheduled job")        
        logging.info("Start Job")
        startprocess()


if __name__ == '__main__':    
    w = Scheduler()


