import os
import sys
import shutil
import logging
import base64
import csv


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

    def get_file(self,path):
      print('')
      a="pepe"
      return a
      # split_name = os.path.splitext(self.path_leaf(path))
      # file_name = split_name[0]
      # print("user name: ", file_name.split("-")[1])
      # logging.info("user name: " + file_name.split("-")[1])
      # return file_name.split("-")[1]
    
    def move_file(self, file):
      if os.path.exists("demofile.txt"):
        shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
      else:
        print("The file does not exist")
        
      print("utils_move")  

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

    def csv_errors(actionlist):
      with open('error.csv', 'w', newline='') as myfile:
          wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
          wr.writerow(actionlist) 

    if __name__ == "__main__":
        # file="Manual LEFEBVRE.pdf"
        # file_tobytearray(file)
        # mylist = [u'value 1', u'value 2', u'value 3']
        # csv_errors(mylist)
        print('main_utils')     

