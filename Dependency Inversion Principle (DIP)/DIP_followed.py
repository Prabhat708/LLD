from abc import ABC, abstractmethod

# Abstract Base Class
class DatabaseSaver(ABC):
    @abstractmethod
    def save(self, cart):
        pass


class SqlDatabaseSaver(DatabaseSaver):
    def save(self, cart):
        print("Saving shopping cart to SQL database...")

class MongoDatabaseSaver(DatabaseSaver):
    def save(self, cart):
        print("Saving shopping cart to MongoDB...")

class Userservice:
    def __init__(self,database: DatabaseSaver):
        self.database = database
    def storeUserData(self,userData):
        self.database.save(userData)

def main():
    sql_saver = SqlDatabaseSaver()
    mongo_saver = MongoDatabaseSaver()

    user_service_sql = Userservice(sql_saver)
    user_service_sql.storeUserData("User data for SQL")

    user_service_mongo = Userservice(mongo_saver)
    user_service_mongo.storeUserData("User data for MongoDB")

if __name__ == "__main__":
    main()

