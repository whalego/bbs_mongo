import datetime
from pymongo import MongoClient


class DBConnection:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("localhost")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


class DBPostMessage(DBConnection):
    def insert_db(self, user_name, text, pict_url=None):
        try:
            post = {
                "author": user_name,
                "text": text,
                "date": datetime.datetime.strftime(datetime.datetime.now(), "%Y%m/%d %H:%M:%S"),
                "pict": pict_url
            }

            self.collection.insert_one(post)
        except Exception as e:
            print(e)
            return "failed"

        return "succeed"

    def show_db_all(self):
        return [x for x in self.collection.find()]


class DBAccount(DBConnection):
    def create_account(self, account, password):
        post = {"Account": account,
                "Password": password
                }
        try:
            if self.search_account(post["Account"]):
                return "Already Exists"
            else:
                self.collection.insert_one(post)
                return "succeed"
        except Exception as e:
            print(e)
            return "failed"

    def search_account(self, account):
        try:
            if account:
                return self.collection.find_one({"Account": account})
        except Exception as e:
            print(e)

        return None


if __name__ == "__main__":
    # db = DBPostMessage("test_database", "test_collection")
    # db = DBAccount("UserDB", "UserCollections")
    # a = db.search_account("_test_user")
    # print(a)
    pass

