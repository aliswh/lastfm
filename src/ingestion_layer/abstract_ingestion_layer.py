from abc import ABC, abstractmethod
 
class Source(ABC):
    @abstractmethod
    def get(self, request) -> str:
        """
        Process a request and return the result.

        """
        pass 


class DataLake(ABC):
    @abstractmethod
    def write(self, data, dest_path:str):
        """
        Write data in the specified destination

        """
        pass
    
    @abstractmethod
    def read(self, path:str):
        """
        Write data from a specified path

        """
        pass


class Writer(ABC):
    @abstractmethod
    def __init__(self, source:Source, destination:DataLake):
        pass

    @abstractmethod
    def write(self, dest_path:str, *args, **kargs):
        """
        Process a request and save in destination.

        """
        pass

