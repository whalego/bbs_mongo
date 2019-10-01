import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


class DBConnection:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("localhost")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]


class DBPostMessage(DBConnection):
    def insert_post(self, user_name, text, pict_url=None, reply=None):
        try:
            if not reply:
                post = {
                    "author": user_name,
                    "text": text,
                    "date": datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S"),
                    "pict": pict_url,
                    "reply": reply,
                    "del_flag": None
                }
            else:
                post = {
                    "author": user_name,
                    "text": f"re: {text}",
                    "date": datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S"),
                    "pict": pict_url,
                    "reply": reply,
                    "del_flag": None
                }
            self.collection.insert_one(post)
        except Exception as e:
            print(e)
            return "failed"

        return "succeed"

    def show_db_all(self):
        # 使わない予定
        return [x for x in self.collection.find()]

    def find_post_for_id(self, search_id):
        return self.collection.find_one({"_id": ObjectId(search_id)})

    def find_post(self, reply_id=None):
        return [x for x in self.collection.find({"reply": reply_id})]

    def delete_post(self, del_id, del_user):
        try:
            self.collection.update_one({"_id": ObjectId(del_id)}, {"$set": {"del_flag": {"name": del_user}}})
        except Exception as e:
            print(e)
            return "failed"
        return "succeed"


class DBAccount(DBConnection):
    def create_account(self, account, password):
        post = {"Account": account,
                "Password": password
                }
        try:
            if self.search_account(post["Account"]):
                return "Already Exists. please another ID."
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
    # a = db.find_reply("5d8c558bb816da8c4d7c5bd6")
    # print(a)
    # db.delete_post("5d82d63a4dbe825064642a42", "asd")
    pass

