# bbs_mongo
Mongodbを使って適当に作った。(そのうち改善する予定)

## 使い方
※忘れないように覚書

環境： Windows10で実施  
cacheディレクトリを対象にMongoDbの立ち上げを実施する。  
windowsのcmdプロンプトより以下を実施しておく。(一回実行したらもう実行しないでいいっぽい？)
```
mongod --dbpath <cahce_directory>
```
※Pycharm上のプロンプトからではなぜか実行できなかった。

実装機能(順不同)  
画像のアップロードを実装した。  
ユーザのログイン機能追加  
ユーザのログアウト機能追加  
ユーザの登録機能追加  
ユーザの削除機能追加  
登録したユーザでなければ投稿出来ないように修正  
登録したユーザ自身の投稿内容を削除出来るように修正  
リプライ機能追加(対象投稿データの詳細からリプライを投稿できるページに飛ぶ。)  
投稿データに対してリプライが見れるように修正  
ユーザの削除と投稿データの削除にはポップアップで確認を求めるように修正した  


### 必要なモジュール
* Flask
* Flask-Login
* Flask-Bcrypt
* pymongo
* Jinja2

