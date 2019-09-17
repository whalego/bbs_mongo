from flask import Flask, render_template, request
from access.mongo import DBConnection
app = Flask(__name__)
db = DBConnection()


@app.route("/")
def index():
    item_list = [{"author": x["author"],
                  "text": x["text"],
                  "date": x["date"]
                  } for x in db.show_db_all()]

    return render_template("/index.html", item_list=item_list)


@app.route("/form", methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        db.insert_db(user_name=req.getlist("text")[0], text=req.getlist("name")[0])
        return index()


if __name__ == "__main__":
    app.run(debug=True)

