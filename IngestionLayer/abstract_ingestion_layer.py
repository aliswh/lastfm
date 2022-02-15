from abc import ABC, abstractmethod
 
class Source(ABC):
    @abstractmethod
    def get(self, request) -> str:
        """
        Process a request and return a path containing the result.

        """
        pass 


class DataLake(ABC):
    @abstractmethod
    def write(self, file_path:str, dest_path:str):
        """
        Write a file in the specified destination

        """
        pass


class Writer(ABC):
    @abstractmethod
    def __init__(self, source:Source, destination:DataLake):
        pass

    @abstractmethod
    def write(self, request, dest_path:str):
        """
        Process a request and save in destination.

        """
        pass
        

class BatchWriter(Writer):
    def __init__(self, source, destination):
        self.source = source
        self.dest = destination

    def write(self, request, dest_path):
        file_path = self.source.get(request)
        self.dest.write(file_path, dest_path)

