import os
import sys
import shutil
import logging
import base64
import csv
import re
import json
import settings
import time
from datetime import datetime, timedelta



from settings import Settings
      


DIRECTORY_TO_MOVE = sys.argv[1] if len(sys.argv) > 1 else '.'  


class Utils:

    def __init__(self):
      
      print('utils_ini')
                        
    def check_file(self,logname):
      # extract the file name and extension
      split_name = os.path.splitext(logname)      
      file_extension = split_name[1]
      if file_extension != ".log":
        return False
      else:
        return True
      
    def path_leaf(self,path):
      return os.path.basename(os.path.normpath(path))
  
    def get_idcompany(self,logname):
      split_name = os.path.splitext(self.path_leaf(logname))
      file_name = split_name[0]
      print("Processing data for client: ", file_name.split("-")[0])
      logging.info("Processing data for client: " + file_name.split("-")[0])
      return file_name.split("-")[0]

    def get_iduser(self,logname):
      split_name = os.path.splitext(self.path_leaf(logname))
      file_name = split_name[0]
      print("user name: ", file_name.split("-")[1])
      logging.info("user name: " + file_name.split("-")[1])
      return file_name.split("-")[1]

        
    def move_file( file):
      try:        
        if not os.path.exists(settings.PROCESSED_LOG_FILES):
          os.makedirs(settings.PROCESSED_LOG_FILES)
          logging.info(f'Making new folder: ' + settings.PROCESSED_LOG_FILES)
        
        if os.path.exists(file):
          shutil.move(file, os.path.join(settings.PROCESSED_LOG_FILES, os.path.basename(file)))          
        else:
          logging.error('Unable to move the file: ' + file + '- file does not exist')
        
        logging.info(file + '- is moved to: ' + settings.PROCESSED_LOG_FILES )  
        
      except OSError as err:
        logging.error("OS error: {0}".format(err))
        print("OS error: {0}".format(err))
        raise
        #return False     
      except BaseException as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        print(f"Unexpected {err=}, {type(err)=}")
        raise
        #return False        
      else:
        return True
      
      

    def delete_file(self, file):
      if os.path.exists("demofile.txt"):
        os.remove("demofile.txt")
      else:
        print("The file does not exist")

      print("utils_delete")  

    def file_tobytearray(self,file):
      try:
        # convert file to bytearray 
        doc = open(file, 'rb').read()   
        data = base64.b64encode(doc)
        print(data)        
      except OSError as err:
        logging.error("OS error: {0}".format(err))
        print("OS error: {0}".format(err))
        raise
        return False     
      except BaseException as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        print(f"Unexpected {err=}, {type(err)=}")
        raise
        return False        
      else:
        return data

    def extact_double_cuotes(text): 
      matches = re.findall(r'"(.+?)"',text)
      # matches is now ['String 1', 'String 2', 'String3']
      return ",".join(matches)

    # def json_errors(actionlist):    
    #   datestr = time.strftime("%Y%m%d") 
    #   if not os.path.exists(settings.ERROR_LOG_FILES):
    #     os.makedirs(settings.ERROR_LOG_FILES)
    #     logging.info(f'Making new folder: ' + settings.ERROR_LOG_FILES)
    #   log_error_file= settings.ERROR_LOG_FILES + '/' + datestr + '.log'
    #   with open(log_error_file, 'a') as outfile:
    #       json.dump(actionlist, outfile)
    #       outfile.write('\n')
    #       logging.info(f'Making new log error : ' + log_error_file)

    def add_error(actionlist):    
      # datestr = time.strftime("%Y%m%d") 
      # if not os.path.exists(settings.ERROR_LOG_FILES):
      #   os.makedirs(settings.ERROR_LOG_FILES)
      #   logging.info(f'Making new folder: ' + settings.ERROR_LOG_FILES)
      # log_error_file= settings.ERROR_LOG_FILES + '/' + datestr + '.log'
      with open(settings.FILENAME_ERROR, 'a') as outfile:
          json.dump(actionlist, outfile)
          outfile.write('\n')
          logging.info(f'Making new log error : ' + settings.FILENAME_ERROR)

    def csv_errors(actionlist):
      with open('error.csv', 'w', newline='') as myfile:
          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
          wr.writerow(actionlist) 
          
    def get_scheduler_next_interval(Sche_time):
        x = datetime.now() + timedelta(seconds=3)
        x += timedelta(seconds=Sche_time)
        return x

    def validateJSON(jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True
      
    if __name__ == "__main__":
        # file="Manual LEFEBVRE.pdf"
        # file_tobytearray(file)
        # mylist = [u'value 1', u'value 2', u'value 3']
        # csv_errors(mylist)
        print('main_utils')     

