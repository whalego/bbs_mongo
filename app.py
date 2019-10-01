from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from access.mongo import DBPostMessage, DBAccount
from pathlib import Path
import datetime

app = Flask(__name__)
app.secret_key = "asd"
db = DBPostMessage("test_database", "test_collection")
account_db = DBAccount("UserDB", "UserCollections")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@app.route("/")
def index():
    item_list = [{"id": x["_id"],
                  "author": x["author"],
                  "text": x["text"],
                  "date": x["date"],
                  "pict": x["pict"],
                  "reply": x["reply"],
                  "del_flag": x["del_flag"]
                  } for x in db.find_post()]
    return render_template("contents/index.html", item_list=item_list)


@app.route("/details", methods=["GET"])
def details():
    if request.method == "GET":
        search_id = request.args.get("post_data")
        id_data = db.find_post_for_id(search_id)
        reply_list = [{"id": x["_id"],
                       "author": x["author"],
                       "text": x["text"],
                       "date": x["date"],
                       "pict": x["pict"],
                       "reply": x["reply"],
                       "del_flag": x["del_flag"]
                       } for x in db.find_post(search_id)]

    return render_template("contents/details.html", post_data=id_data, reply_list=reply_list)


@app.route("/post_form", methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        pict = save_picture(request.files["pict"])
        if current_user.is_authenticated:
            result = db.insert_post(user_name=current_user.id,
                                    text=req.getlist("text")[0],
                                    pict_url=pict
                                    )
            flash(result)
        else:
            flash("投稿失敗")
    return redirect(url_for("index"))


@app.route("/details/reply_form", methods=["POST"])
def replay_form():
    # 普通のフォームと書き方が同じなので、対策を考える。
    if request.method == "POST":
        req = request.form
        if current_user.is_authenticated:
            result = db.insert_post(user_name=current_user.id,
                                    text=req.getlist("text")[0],
                                    reply=req.getlist("reply")[0]
                                    )
            flash(result)
        else:
            flash("投稿失敗")
    return redirect(url_for("details", post_data=req.getlist("reply")[0]))


@app.route("/del_post", methods=["POST"])
def del_form():
    if request.method == "POST":
        req = request.form
        db.delete_post(req.getlist("id")[0], current_user.id)

    return redirect(url_for("index"))


@app.route("/login_form", methods=["POST"])
def login_form():
    if request.method == "POST":
        crypt = Bcrypt(app)
        user = User(request.form["account"])
        if user.info is not None and crypt.check_password_hash(user.info["Password"], request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("login failed")

    return redirect(url_for("index"))


@app.route("/create_account", methods=["POST"])
def create_account():
    if request.method == "POST":
        account_name = request.form["account"]
        password = request.form["password"]
        if len(password) >= 6:
            crypt = Bcrypt(app)
            hash_password = crypt.generate_password_hash(password)
            result = account_db.create_account(account_name, hash_password)

        else:
            result = "you type password is short! change password please."

        flash(result)

    return redirect(url_for("index"))


@app.route("/logout_form", methods=["POST"])
def logout_form():
    if request.method == "POST":
        logout_user()

    return redirect(url_for("index"))


class User(UserMixin):
    def __init__(self, name):
        self.id = name
        self.info = self._get_id()

    def _get_id(self):
        return account_db.search_account(self.id)


@login_manager.user_loader
def user_loader(account_name):
    user = User(account_name)
    if user.info and account_name == user.info["Account"]:
        return user
    return None


@login_manager.request_loader
def request_loader(req):
    try:
        user = User(req.form["account"])
        if user.info and user.info["Account"] != req.form["account"]:
            return None
        user.is_authenticated = req.form["account"] == user.info["Password"]
        return user
    except Exception as e:
        # ログアウト時に 400 bad request が発生する。
        return redirect(url_for("index"))


def save_picture(picture):
    cache_dir = Path(r"static/picture/")
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

