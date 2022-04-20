from asyncore import loop
import logging
import time
import glob
import datetime
import settings
import parser
import queuemanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from schedule import every, repeat, run_pending

## logging configuration 
logging.basicConfig(filename='monitor.log', encoding='utf-8',level=logging.NOTSET,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

## settigs 
settings.Settings.init() # Call only once

#logging
logging.debug("PROCESSED_FILES ------ " + settings.PROCESSED_FILES)
logging.debug("ERROR_FILES ---------- " + settings.ERROR_FILES)
logging.debug("DIRECTORY_TO_WATCH --- " + settings.DIRECTORY_TO_WATCH)
logging.debug("LOGGING_LEVEL -------- " + settings.LOGGING_LEVEL)
logging.debug("QUEUE_TIME ----------- " + str(settings.QUEUE_TIME))
logging.debug("SCHEDULE_TIME -------- " + str(settings.SCHEDULER_TIME_INTERVAL))
logging.debug("MAX_RETRIES ---------- " + str(settings.MAX_RETRIES))


#print screen
print ("PROCESSED_FILES ------ " + settings.PROCESSED_FILES) 
print ("ERROR_FILES ---------- " + settings.ERROR_FILES) 
print ("DIRECTORY_TO_WATCH --- " + settings.DIRECTORY_TO_WATCH) 
print ("LOGGING_LEVEL -------- " + settings.LOGGING_LEVEL) 
print ("QUEUE_TIME ----------- " + str(settings.QUEUE_TIME)) 
print ("SCHEDULE_TIME -------- " + str(settings.SCHEDULER_TIME_INTERVAL))
print ("MAX_RETRIES ---------- " + str(settings.MAX_RETRIES))


## var to customize
##path_to_rclone_log_folder = r'LogRsync\*'
path_to_rclone_log_folder = settings.DIRECTORY_TO_WATCH + "\*"

## all possible action of rclone  
possible_action_rclone= ['logpath','stats','Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']
    
## start main process
def startprocess ():
    ## get all log files of rclone_log_folder
    inxforTrhead=0
    QueueProcess = queuemanager.Queue()
    for logpath in glob.glob(path_to_rclone_log_folder):
        inxforTrhead = inxforTrhead + 1
        print("\n\n\n++++++++ PROCESING LOG " + logpath + "+++++++++++++")
        with open(logpath,errors='ignore') as f:  # errors='ignore' : when strange character in log -then ignore
            content = f.readlines()
            list_of_actions_from_log = [x.strip() for x in content]

        ## read log and store each line in 
        datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
        # print(f"{datetime.datetime.now():%Y/%m/%d}")
        datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
        print("\n+++++++++++++ All actions +++++++++++++\n")
        log_actions = parser.select_actions_based_on_condition(datetime_beginning_of_time, logpath, list_of_actions_from_log)

        # check if log processed is ok
        if  log_actions == False:
            logging.critical("ERROR LOG FILE FORMAT: " + logpath)
            print ("ERROR LOG FILE FORMAT: " + logpath)
            continue
        
        # Add the process to the main queue
        logging.debug("Main Queue" + " (#" + str(inxforTrhead) + ") " + "start - " + logpath)
        print ("Main Queue" + " (#" + str(inxforTrhead) + ") " + "start - " + logpath)
        QueueProcess.main(log_actions,inxforTrhead)

## main class
class Scheduler: 
        
    def __init__(self):
        logging.info("Start Job on start")        
        startprocess()
        
        logging.debug("Starting Observer")        
        self.observer = Observer()

        while True:
            run_pending()
            time.sleep(1)

    ## start the timer
    @repeat(every(settings.SCHEDULER_TIME_INTERVAL).seconds)
    def job():
        print("start scheduled job")
        startprocess()


if __name__ == '__main__':       
    w = Scheduler()


