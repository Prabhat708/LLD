'''A cloud application supports AWS and Azure. Each cloud provider needs Storage, Compute and Queue services from the same provider.'''

from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def use(self):
        pass
class Compute(ABC):
    @abstractmethod
    def use(self):
        pass
class Queue(ABC):
    @abstractmethod
    def use(self):
        pass

class AWSStorage(Storage):
    def use(self):
        return "Creating AWS S3 Storage"
class AWSCompute(Compute):
    def use(self):
        return "Creating AWS EC2 Compute"
class AWSQueue(Queue):
    def use(self):
        return "Creating AWS SQS Queue"

class AzureStorage(Storage):
    def use(self):
        return "Creating Azure Blob Storage"
class AzureCompute(Compute):
    def use(self):
        return "Creating Azure Virtual Machines Compute"
class AzureQueue(Queue):
    def use(self):
        return "Creating Azure Storage Queue"

class CloudProviderFactory(ABC):
    @abstractmethod
    def create_storage(self):
        pass
    @abstractmethod
    def create_compute(self):
        pass
    @abstractmethod
    def create_queue(self):
        pass

class AWSFactory(CloudProviderFactory):
    def create_storage(self):
        return AWSStorage()
    def create_compute(self):
        return AWSCompute()
    def create_queue(self):
        return AWSQueue()

class AzureFactory(CloudProviderFactory):
    def create_storage(self):
        return AzureStorage()
    def create_compute(self):
        return AzureCompute()
    def create_queue(self):
        return AzureQueue()

if __name__ == "__main__":
    provider = input("Enter cloud provider (aws/azure): ").lower()

    if provider == "aws":
        factory = AWSFactory()
    elif provider == "azure":
        factory = AzureFactory()
    else:
        print("Invalid cloud provider")
        exit(1)

    storage = factory.create_storage()
    compute = factory.create_compute()
    queue = factory.create_queue()

    print(storage.use())
    print(compute.use())
    print(queue.use())