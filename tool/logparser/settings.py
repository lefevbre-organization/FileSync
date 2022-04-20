import yaml

class Settings:
    
    def init():

        with open("config.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    
        global PROCESSED_FILES 
        global ERROR_FILES
        global DIRECTORY_TO_WATCH
        global LOGGING_LEVEL
        global QUEUE_TIME
        global SCHEDULER_TIME_INTERVAL
        global MAX_RETRIES
        
        PROCESSED_FILES = cfg["app_paths"]["processed_files"]
        ERROR_FILES= cfg["app_paths"]["error_files"]       
        DIRECTORY_TO_WATCH = cfg["watcher"]["directory"] 
        LOGGING_LEVEL = cfg["logging"]["level"]
        QUEUE_TIME = float(cfg["queue"]["time"] )
        SCHEDULER_TIME_INTERVAL = float(cfg["scheduler"]["time_interval"] )       
        MAX_RETRIES = int(cfg["other"]["max_retries"] )

    if __name__ == "__main__":
        init()
        print('settings_main')
