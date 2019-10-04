import os
# Flaskを実行するための設定ファイル

# 実行する前に必ず変更する。
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "SECRET_KEY"

# MongoDBで利用する
## 投稿データ管理DB
POST_DB_NAME = "Post_db"
POST_DB_COLLECTION_NAME = "Post_collection"
## アカウント管理DB
ACCOUNT_DB_NAME = "User_db"
ACCOUNT_DB_COLLECTION_NAME = "User_collection"
