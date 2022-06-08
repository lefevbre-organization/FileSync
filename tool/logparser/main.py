from asyncore import loop
from email import utils
import logging
import time
import os
import glob
import datetime
import settings
import parser
import queuemanager
import logginfilehandler
import errorfilehandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from schedule import every, repeat, run_pending
import api
from utils import Utils

## archive logging
hdler = logginfilehandler.CustomLoggingFileHandler(settings.FILENAME_LOGGING)
## logging configuration
logging.basicConfig(encoding='utf-8', level=logging.NOTSET, handlers=[hdler], 
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

## archive errors
hdlerror = errorfilehandler.CustomErrorFileHandler(settings.FILENAME_ERROR)


## settigs 

#logging
logging.debug("PROCESSED_FILES ------ " + settings.PROCESSED_LOG_FILES)
logging.debug("DIRECTORY_TO_WATCH --- " + settings.DIRECTORY_TO_WATCH)
logging.debug("LOGGING_LEVEL -------- " + settings.LOGGING_LEVEL)
logging.debug("QUEUE_TIME ----------- " + str(settings.QUEUE_TIME))
logging.debug("SCHEDULE_TIME -------- " + str(settings.SCHEDULER_TIME_INTERVAL))
logging.debug("MAX_RETRIES ---------- " + str(settings.MAX_RETRIES))
logging.debug("MAX_TIMEOUT ---------- " + str(settings.MAX_TIMEOUT))
logging.debug("ENDPOINT_TO_CHECK ---- " + str(settings.ENDPOINT_TO_CHECK))
logging.debug("FILENAME_LOGGING ----- " + str(settings.FILENAME_LOGGING))
logging.debug("ARCHIVE_LOGGING ------ " + str(settings.ARCHIVE_LOGGING))
logging.debug("FILENAME_ERROR ------- " + str(settings.FILENAME_ERROR))
logging.debug("ARCHIVE_ERROR -------- " + str(settings.ARCHIVE_ERROR))
logging.debug("CUSTOMERS_SOURCE_BASE -" + str(settings.CUSTOMERS_SOURCE_BASE))
logging.debug("ARCHIVE_FOLDER -" + str(settings.ARCHIVE_FOLDER))

#print screen
print ("PROCESSED_LOG_FILES ------ " + settings.PROCESSED_LOG_FILES) 
print ("DIRECTORY_TO_WATCH ------- " + settings.DIRECTORY_TO_WATCH) 
print ("LOGGING_LEVEL ------------ " + settings.LOGGING_LEVEL) 
print ("QUEUE_TIME --------------- " + str(settings.QUEUE_TIME)) 
print ("SCHEDULE_TIME ------------ " + str(settings.SCHEDULER_TIME_INTERVAL))
print ("MAX_RETRIES -------------- " + str(settings.MAX_RETRIES))
print ("MAX_TIMEOUT ---------- --- " + str(settings.MAX_TIMEOUT))
print ("ENDPOINT_TO_CHECK -------- " + str(settings.ENDPOINT_TO_CHECK))
print ("FILENAME_LOGGING --------- " + str(settings.FILENAME_LOGGING))
print ("ARCHIVE_LOGGING ---------- " + str(settings.ARCHIVE_LOGGING))
print("FILENAME_ERROR ------------ " + str(settings.FILENAME_ERROR))
print("ARCHIVE_ERROR ------------- " + str(settings.ARCHIVE_ERROR))
print("CUSTOMERS_SOURCE_BASE ----- " + str(settings.CUSTOMERS_SOURCE_BASE))
print("ARCHIVE_FOLDER -" + str(settings.ARCHIVE_FOLDER))

## var to customize
##path_to_rclone_log_folder = r'LogRsync\*'

if os.name == 'nt':
    path_to_rclone_log_folder = settings.DIRECTORY_TO_WATCH + "\*"
else:
    path_to_rclone_log_folder = settings.DIRECTORY_TO_WATCH + "/*"

## all possible action of rclone  
possible_action_rclone= ['logpath','stats','Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']

def main ():
    try: 
        startprocess()
    except BaseException as err:
        logging.error({"message": err})
        return False
        
## start main process
def startprocess ():

    
    
    ## check if endpints are ok
    if  api.method_check(settings.ENDPOINT_TO_CHECK) == False:
        logging.critical("The checked EndPoint is DOWN")
        print ("The checked EndPoint is DOWN")
        
        logging.debug("Waiting for the next scheduler at " + str(Utils.get_scheduler_next_interval(settings.SCHEDULER_TIME_INTERVAL)) )
        print ("Waiting for the next scheduler at " + str(Utils.get_scheduler_next_interval(settings.SCHEDULER_TIME_INTERVAL)) )
        
        return
    
    ## get all log files of rclone_log_folder
    inxforTrhead=0
    QueueProcess = queuemanager.Queue()
    if len(glob.glob(path_to_rclone_log_folder)) > 0:
        # try:
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
                
                # Finally Move log file to the selected processed folder
                Utils.move_file(logpath)
                
        # except BaseException as err:
        #     logging.error({"message": err})
            
    else:
        logging.info("Nothing to proccess in: " + path_to_rclone_log_folder)
        print("Nothing to proccess at: " + path_to_rclone_log_folder)

    time.sleep(1)    
    logging.debug("Waiting for the next scheduler at " + str(Utils.get_scheduler_next_interval(settings.SCHEDULER_TIME_INTERVAL)) )
    print ("Waiting for the next scheduler at " + str(Utils.get_scheduler_next_interval(settings.SCHEDULER_TIME_INTERVAL)) )

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


