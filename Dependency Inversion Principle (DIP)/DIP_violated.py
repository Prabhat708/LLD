# Low-level module
class MySQLDatabase:
    def save_to_sql(self, data):
        print(f"Executing SQL Query: INSERT INTO users VALUES('{data}');")


# Low-level module
class MongoDBDatabase:
    def save_to_mongo(self, data):
        print(f"Executing MongoDB Function: db.users.insert({{'name': '{data}'}})")


# High-level module (Tightly coupled)
class UserService:
    def __init__(self):
        self.sql_db = MySQLDatabase()      # Direct dependency on MySQL
        self.mongo_db = MongoDBDatabase()  # Direct dependency on MongoDB

    def store_user_to_sql(self, user):
        # MySQL-specific code
        self.sql_db.save_to_sql(user)

    def store_user_to_mongo(self, user):
        # MongoDB-specific code
        self.mongo_db.save_to_mongo(user)


def main():
    service = UserService()

    service.store_user_to_sql("Aditya")
    service.store_user_to_mongo("Rohit")


if __name__ == "__main__":
    main()