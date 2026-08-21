from abc import ABC, abstractmethod


# Interface
class IDataService(ABC):

    @abstractmethod
    def fetch_data(self):
        pass


# Real Object
class RealDataService(IDataService):

    def __init__(self):
        # Imagine this connects to a remote server
        # or loads heavy resources.
        print("[RealDataService] Initialized (simulating remote setup)")

    def fetch_data(self):
        return "[RealDataService] Data from server"


# Remote Proxy
class DataServiceProxy(IDataService):

    def __init__(self):
        self.real_service = RealDataService()

    def fetch_data(self):
        print("[DataServiceProxy] Connecting to remote service...")
        return self.real_service.fetch_data()


# Client
if __name__ == "__main__":

    data_service = DataServiceProxy()

    print(data_service.fetch_data())