import logging
import os
import settings
import errno
from datetime import datetime


class CustomErrorFileHandler(logging.FileHandler):

    def __init__(self, filename, archive_path=settings.ARCHIVE_ERROR, archive_name='error_%Y%m%d', **kwargs):

        try:
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise 
            
        self._archive = os.path.join(archive_path, archive_name)
        self._archive_error(filename)
        super().__init__(filename, **kwargs)

    def _archive_error(self, filepath):
        if os.path.exists(filepath):
            if not os.path.exists(datetime.now().strftime(self._archive)):
                os.rename(filepath, datetime.now().strftime(self._archive))

    def close(self):
        super().close()
        self._archive_error(self.baseFilename)

if __name__ == "__main__":
        #main()
        print('CustomErrorFileHandler_main_')