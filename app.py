from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from access.mongo import DBConnection
from pathlib import Path
import datetime
from PIL import Image
import io
app = Flask(__name__)
app.secret_key = "asd"
db = DBConnection()


@app.route("/")
def index(message=""):
    item_list = [{"author": x["author"],
                  "text": x["text"],
                  "date": x["date"],
                  "pict": x["pict"],
                  } for x in db.show_db_all()]

    return render_template("/index.html", item_list=item_list, db_log=message)


@app.route("/form", methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        pict = save_picture(request.files["pict"])

        result = db.insert_db(user_name=req.getlist("text")[0],
                              text=req.getlist("name")[0],
                              pict_url=pict
                              )
        if pict is None:
            flash("you upload file is not image file, image upload is failed.")
        else:
            flash(result)
    return redirect(url_for("index"))


def save_picture(picture):
    cache_dir = Path(r"/static/picture/")
    suffix = ["png", "jpg", "bmp", "gif"]

    pict_suffix = picture.filename.split(".")[-1]
    if pict_suffix in suffix:
        now_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
        pict_url = str(Path(cache_dir, now_time + "." + pict_suffix))
        picture.save(pict_url)
    else:
        pict_url = None

    return pict_url


if __name__ == "__main__":
    app.run(debug=True)

