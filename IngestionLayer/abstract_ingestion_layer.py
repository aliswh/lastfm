from abc import ABC, abstractmethod
 
class Source(ABC):
    @abstractmethod
    def Get(self, request) -> str:
        """
        Process a request and return a path containing the result.

        """
        pass 


class DataLake(ABC):
    @abstractmethod
    def Write(self, file_path:str, dest_path:str):
        """
        Write a file in the specified destination

        """
        pass


class Writer(ABC):
    @abstractmethod
    def __init__(self, source:Source, destination:DataLake):
        pass

    @abstractmethod
    def Write(self, request, dest_path:str):
        """
        Process a request and save in destination.

        """
        pass
        
        
class BatchWriter(Writer):
    def __init__(self, source, destination):
        self.source = source
        self.dest = destination

    def Write(self, request, dest_path):
        file_path = self.source.Get(request)
        self.dest.Write(file_path, dest_path)

