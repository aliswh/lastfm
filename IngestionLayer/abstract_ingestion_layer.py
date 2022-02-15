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
        data = self.source.get(request)
        self.dest.write(data, dest_path)

