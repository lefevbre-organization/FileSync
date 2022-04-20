import os
import sys
import shutil
import logging
import base64


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
  
    def get_client(self,logname):
      split_name = os.path.splitext(self.path_leaf(logname))
      file_name = split_name[0]
      print("Processing data for client: ", file_name.split("-")[0])
      logging.info("Processing data for client: " + file_name.split("-")[0])
      return file_name.split("-")[0]

    def get_user(self,logname):
      split_name = os.path.splitext(self.path_leaf(logname))
      file_name = split_name[0]
      print("user name: ", file_name.split("-")[1])
      logging.info("user name: " + file_name.split("-")[1])
      return file_name.split("-")[1]
      
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
      # convert file to bytearray 
      doc = open(file, 'rb').read()   
      data = base64.b64encode(doc)
      print(data)
      return data

    if __name__ == "__main__":
        # file="Manual LEFEBVRE.pdf"
        # file_tobytearray(file)
        print('main_utils')     

