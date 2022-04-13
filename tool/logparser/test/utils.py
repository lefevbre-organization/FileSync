import os
import sys
import shutil


DIRECTORY_TO_MOVE = sys.argv[1] if len(sys.argv) > 1 else '.'  


class Utils:

    def __init__(self):
      print('utils_ini')
                        
    
    def move(self, file):
      if os.path.exists("demofile.txt"):
        shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
      else:
        print("The file does not exist")
        
      print("utils_move")  

    def delete(self, file):
      if os.path.exists("demofile.txt"):
        os.remove("demofile.txt")
      else:
        print("The file does not exist")

      print("utils_delete")  
        

