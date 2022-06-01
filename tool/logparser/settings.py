import yaml

class Settings:
    
    def init():

        with open("config.yaml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
        global PROCESSED_LOG_FILES       
        global DIRECTORY_TO_WATCH
        global LOGGING_LEVEL
        global QUEUE_TIME
        global SCHEDULER_TIME_INTERVAL
        global MAX_RETRIES
        global MAX_TIMEOUT
        global ENDPOINT_TO_CHECK
        global FILENAME_LOGGING
        global ARCHIVE_LOGGING
        global FILENAME_ERROR
        global ARCHIVE_ERROR
        global CUSTOMERS_SOURCE_BASE
        global ARCHIVE_FOLDER
        
        PROCESSED_LOG_FILES = cfg["app_paths"]["processed_log_files"]
        DIRECTORY_TO_WATCH = cfg["watcher"]["directory"] 
        LOGGING_LEVEL = cfg["logging"]["level"]
        QUEUE_TIME = float(cfg["queue"]["time"] )
        SCHEDULER_TIME_INTERVAL = float(cfg["scheduler"]["time_interval"] )       
        MAX_RETRIES = int(cfg["other"]["max_retries"] )
        MAX_TIMEOUT = int(cfg["other"]["timeout"] )
        ENDPOINT_TO_CHECK = cfg["other"]["endpoint_to_check"]
        FILENAME_LOGGING = cfg["logging"]["filename"]
        ARCHIVE_LOGGING = cfg["logging"]["archive"]
        FILENAME_ERROR = cfg["error"]["filename"]
        ARCHIVE_ERROR = cfg["error"]["archive"]
        CUSTOMERS_SOURCE_BASE = cfg["app_paths"]["customers_source_base"]
        ARCHIVE_FOLDER = cfg["app_paths"]["archive_folder"]

    if __name__ == "__main__":
        init()
        print('settings_main')
