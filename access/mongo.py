import datetime
from pymongo import MongoClient


class DBConnection:
    def __init__(self):
        self.client = MongoClient("localhost")
        self.db = self.client.test_database
        self.collection = self.db.test_collection

    def insert_db(self, user_name, text, pict_url=""):
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

    def insert_db_many(self):
        pass

    def show_db_all(self):
        return [x for x in self.collection.find()]
