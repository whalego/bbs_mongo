# bbs_mongo
Mongodbを使って適当に作った。(そのうち改善する予定)

## 使い方
※忘れないように覚書

cacheディレクトリを対象にMongoDbの立ち上げを実施する。  
windowsのcmdプロンプトより以下を実施しておく。
```
mongod --dbpath <cahce_directory>
```
※Pycharm上のプロンプトからではなぜか実行できなかった。

画像のアップロードを実装した。  
ユーザのログイン機能追加(登録機能は作成していない。)  
登録したユーザでなければ投稿出来ないように修正  
登録したユーザ自身の投稿内容を削除出来るように修正  

### 必要なモジュール
* Flask
* Flask-Login
* Flask-Bcrypt
* pymongo
* Jinja2

