import yaml

class Settings:
    
    def init():

        with open("config.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


    
        global PROCESSED_LOG_FILES 
        global ERROR_LOG_FILES
        global DIRECTORY_TO_WATCH
        global LOGGING_LEVEL
        global QUEUE_TIME
        global SCHEDULER_TIME_INTERVAL
        global MAX_RETRIES
        global MAX_TIMEOUT
        global ENDPOINT_TO_CHECK
        global ARCHIVE_LOGGING
        
        PROCESSED_LOG_FILES = cfg["app_paths"]["processed_log_files"]
        ERROR_LOG_FILES= cfg["app_paths"]["error_log_files"]       
        DIRECTORY_TO_WATCH = cfg["watcher"]["directory"] 
        LOGGING_LEVEL = cfg["logging"]["level"]
        QUEUE_TIME = float(cfg["queue"]["time"] )
        SCHEDULER_TIME_INTERVAL = float(cfg["scheduler"]["time_interval"] )       
        MAX_RETRIES = int(cfg["other"]["max_retries"] )
        MAX_TIMEOUT = int(cfg["other"]["max_retries"] )
        ENDPOINT_TO_CHECK = cfg["other"]["endpoint_to_check"]
        ARCHIVE_LOGGING = cfg["logging"]["archive"]

    if __name__ == "__main__":
        init()
        print('settings_main')
