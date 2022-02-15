from abc import ABC, abstractmethod
 
class Source(ABC):
    @abstractmethod
    def __init__(self, fileType:str):
        pass

    @abstractmethod
    def Get(request:str) -> str:
        """
        Process a request and return a path containing the result.

        """
        pass


class DataLake(ABC):
    @abstractmethod
    def Write(file_path:str, dest_path:str):
        """
        Write a file in the specified destination

        """
        pass


class Writer(ABC):
    @abstractmethod
    def __init__(self, source:Source, destination:DataLake):
        pass
    
    @abstractmethod
    def Write(request:str, dest_path:str):
        """
        Process a request and save in destination.

        """
        pass
        

