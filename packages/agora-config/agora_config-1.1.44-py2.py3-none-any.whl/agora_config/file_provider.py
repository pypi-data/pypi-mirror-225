import json
import pathlib
from agora_logging import logger
from .dict_of_dict import DictOfDict


class FileProvider(DictOfDict):
    def __init__(self, filename):
        super().__init__()
        self.config_file = pathlib.Path(filename)
        if filename == "AEA.json":
            self.primary = True
        else:
            self.primary = False
        self.last_modified_time = 0
        self.__check_time()

    def check_for_updates(self) -> bool:
        return self.__check_time()

    def get_config_file_type(self) -> str:
        if self.primary:
            return 'PRIMARY'
        return 'ALTERNATE'

    # private methods

    def __read_config(self) -> dict:
        """
        Reads the configuration file
        """
        self.clear()
        if self.config_file.exists():
            data = self.config_file.read_text()
            try:
                self.merge(json.loads(data))
            except Exception as e:
                logger.exception(
                    e, f"Could not load {self.get_config_file_type()} config file '{self.config_file}' : {str(e)}")
                self.clear()

    def __check_time(self) -> bool:
        """
        Checks if the time on the configuration file has changed
        """
        mtime = 0
        if self.config_file.exists():
            try:
                mtime = self.config_file.stat().st_mtime
            except Exception as e:
                logger.exception(
                    e, f"Could not get {self.get_config_file_type()} config file time. (config_file = '{self.config_file}')")
                return False
            if mtime != self.last_modified_time:
                self.__read_config()
                self.last_modified_time = mtime
                return True
        else:
            # print( f"file = '{self.config_file.absolute()}' - does not exist")
            super().clear()
        return False
