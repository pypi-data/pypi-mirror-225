import sys
import os.path
import ctypes as C
from ctypes.wintypes import HMODULE
import platform

import logging

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.addHandler(logging.NullHandler())

class SharedLibrayLoader:
    def __init__(self):
        self.open_count = 0
        self.libraries = dict()
    
    def increment(self):
        if (self.open_count == 0):
            self._load_all()
        self.open_count = self.open_count + 1
    
    def decrement(self):
        self.open_count = self.open_count - 1
        if (self.open_count == 0):
            self._free_all()
    
    def _load_all(self):

        if platform.architecture()[0] != "64bit":
            logger.error("Python Interpreter not x64")
            raise OSError

        dll_path = os.path.dirname(__file__).replace("\\", "/")

        if sys.platform.startswith('win32'):
            self._sdk_name = "sc2_cam.dll"
            self._recorder_name = "pco_recorder.dll"
            self._convert_name = "pco_conv.dll"
        elif sys.platform.startswith('linux'):
            self._sdk_name = "libpco_sc2cam.so.1"
            self._recorder_name = "libpco_recorder.so.3"
            self._convert_name = "libpco_convert.so.1"
        else:
            logger.error("Package not supported on platform " + sys.platform)
            raise SystemError
        
        # set working directory
        # workaround, due to implicit load of PCO_File.dll
        current_working_directory = os.getcwd()
        os.chdir(dll_path)

        try:
            if sys.platform.startswith('win32'):
                self.libraries["sdk"] = C.windll.LoadLibrary(dll_path + "/" + self._sdk_name)
                self.libraries["recorder"] = C.windll.LoadLibrary(dll_path + "/" + self._recorder_name)
                self.libraries["convert"] = C.windll.LoadLibrary(dll_path + "/" + self._convert_name)
            else:  # if sys.platform.startswith('linux'):
                self.libraries["sdk"] = C.cdll.LoadLibrary(dll_path + "/" + self._sdk_name)
                self.libraries["recorder"] = C.cdll.LoadLibrary(dll_path + "/" + self._recorder_name)
                self.libraries["convert"] = C.cdll.LoadLibrary(dll_path + "/" + self._convert_name)
        except OSError:
            logger.error(
                'Error: "'
                + self._sdk_name
                + '" not found in directory "'
                + dll_path
                + '".'
            )
            os.chdir(current_working_directory)
            raise
        
        os.chdir(current_working_directory)       

    def _free_all(self):
        try:
            if sys.platform.startswith('win32'):
                C.windll.kernel32.FreeLibrary.argtypes = [HMODULE]
                C.windll.kernel32.FreeLibrary(self.libraries["convert"]._handle)
                C.windll.kernel32.FreeLibrary(self.libraries["recorder"]._handle)
                C.windll.kernel32.FreeLibrary(self.libraries["sdk"]._handle)
            else:  # if sys.platform.startswith('linux'):
                C.cdll.dlclose(self.libraries["convert"]._handle)
                C.cdll.dlclose(self.libraries["recorder"]._handle)
                C.cdll.dlclose(self.libraries["sdk"]._handle)

        except Exception as exc:
            logger.error("FreeLibrary: {}".format(exc))


    def libs(self):
        return self.libraries

shared_library_loader = SharedLibrayLoader()