import logging
import time
import sys
import logging
import requests

from schedule import every, repeat, run_pending

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


DIRECTORY_TO_WATCH = sys.argv[1] if len(sys.argv) > 1 else '.'

#path = sys.argv[1] if len(sys.argv) > 1 else '.'

logging.basicConfig(filename='monitor.log', encoding='utf-8',level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
    
class Watcher:
    
    def __init__(self):
        

        while True:
            self.observer = Observer()
            run_pending()
            time.sleep(1)
            
            
        

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()
        
    @repeat(every(10).seconds)
    def job():
        print("I am a scheduled job")
        
        logging.info("Start Job")

        # Create a new resource
        response = requests.post('https://httpbin.org/post', data = {'key':'value'})
        print (response)
        # Update an existing resource
        requests.put('https://httpbin.org/put', data = {'key':'value'})
        print (response)

        if (response.status_code == 200):
            print("The request was a success!")
        # Code here will only run if the request is successful
        elif (response.status_code) == 404:
            print("Result not found!")
            # Code here will react to failed requests
        
    
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()
