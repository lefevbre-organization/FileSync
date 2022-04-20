import queue
import threading
import time
import json
import logging
import settings
import api
import utils 
from pathlib import Path

## settigs 
settings.Settings.init() # Call only once

## utils
util = utils.Utils() # Call only once

## queues

# main queue
def main_queue(q, thread_no,log_actions ):
    while True:
        task = q.get()
        time.sleep(settings.QUEUE_TIME) 
        logging.debug(f'Thread #{thread_no} is doing task #{task} in the main queue.')       
        print(f'Thread #{thread_no} is doing task #{task} in the main queue.')
        orchestration_process(log_actions)
        q.task_done()
        print(f'Thread #{thread_no} completed #{task} of the main queue.')
        logging.debug(f'Thread #{thread_no} completed #{task} of the main queue.')
        
        
# restful queue
def restful_queue(qApi, thread_no,log_action):
    # json_object = json.loads(log_action)
    while True:
        task = qApi.get() + ' ' + log_action['object']
        time.sleep(settings.QUEUE_TIME)        
        print(f'Thread #{thread_no} is doing task #{task} in the api queue.')
        logging.debug(f'Thread #{thread_no} is doing task #{task} in the api queue.')
        #select Swich method depending action
        #if key is deleted
        api = api_method_switcher(log_action)        
        qApi.task_done()        
        print(f'Thread #{thread_no} completed #{task} of the api queue with result: #{api}.')
        logging.debug(f'Thread #{thread_no} completed #{task} of the api queue with result: #{api}.')
        
            

## Api Method switcher
def api_method_switcher(log_action):
    try:
        #if Key is Copied (new)
        if log_action['msg'] == "Copied (new)":
            filename = Path(log_action['client'] + "/" + log_action['object'])            
            data= util.file_tobytearray(filename)
            api.method_post(log_action,data) 
        #elseif key is Copy...
        #api.method_post(log_action)
        #elseif key is rename 
        #api.method_put(log_action) 
    
        #api.method_delete(log_action)
    except OSError as err:
        logging.error("OS error: {0}".format(err))
        print("OS error: {0}".format(err))
        return False
    except ValueError:
        logging.error("Could not convert data to an integer.")
        print("Could not convert data to an integer.")
        return False
    except BaseException as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        print(f"Unexpected {err=}, {type(err)=}")
        #raise
        return False        
    else:
        return True
    
    
## orchestration
def orchestration_process(log_actions):	
    empty_keys=[]  # if key empty, don't display it
    for key, value in log_actions.items():
        if len(value) != 0:	
            print('\n')
            print('*******' + key+'*******')
            print('number of files: ', len(value))
            print(('\n').join(value))
            ## Orchesting to differents enpoints depending of action type
            ## excludig the "Other", "logpath" , and "stats" tags		
            if (key != "Others" and key != "logpath" and key != "stats" and key != "client"):
                task_thread_dispatcher(key,value)           

        else:               
            empty_keys.append(key)                        
            #print("Actions not done:" + (', ').join(empty_keys))

## thread dispatcher
def task_thread_dispatcher(key, actionCollection):
    #new queue (restful calls) and one thread for each action or methods to call
    inxtasks = 0
    qApi = queue.Queue()
    for i in actionCollection:        
        inxtasks = inxtasks + 1
        workerApi = threading.Thread(target=restful_queue, args=(qApi,inxtasks, json.loads(i)), daemon=True)
        workerApi.start()
        qApi.put('api_action: ' + key)		
    qApi.join()
    print('All work of restful_queue is completed') 
        
class Queue:    
    def __init__(self):
        print('main_queue_init_')        
    def main(self,log_actions, inxforTrhead ):        
        logpath = ''.join(str(e) for e in log_actions['logpath'])      
        # new queue (main) into the the thread 
        logging.debug("Main Queue" + " (#" + str(inxforTrhead) + ") " + "init - " + logpath)
        print("Main Queue" + " (#" + str(inxforTrhead) + ") " + "init - " + logpath)     
        q = queue.Queue()		
        worker = threading.Thread(target=main_queue, args=(q, inxforTrhead,log_actions), daemon=True)
        worker.start()
        q.put(logpath)		
        q.join()
        logging.debug("Main Queue" + " (#" + str(inxforTrhead) + ") " + "join completed - " + logpath)
        print("Main Queue" + " (#" + str(inxforTrhead) + ") " + "join completed - " + logpath)     
        
    if __name__ == "__main__":
        #main()
        print('main_queuemanager_main_')