from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
from access.mongo import DBPostMessage, DBAccount
from pathlib import Path
import base64

app = Flask(__name__)
app.secret_key = "asd"
db = DBPostMessage("test_database", "test_collection")
account_db = DBAccount("UserDB", "UserCollections")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@app.route("/")
def index():
    try:
        item_list = [{"id": x["_id"],
                      "author": x["author"],
                      "text": x["text"],
                      "date": x["date"],
                      "pict": x["pict"],
                      "reply": x["reply"],
                      "del_flag": x["del_flag"]
                      } for x in db.find_post()]
    except Exception as e:
        print(e)
        abort(500)
    return render_template("contents/index.html", item_list=item_list)


@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(500)
def server_error(event):
    return render_template("error/page_errors.html", event=event)


@app.route("/details", methods=["GET"])
def details():
    try:
        if request.method == "GET":
            search_id = request.args.get("post_data")
            id_data = db.find_post_for_id(search_id)
            if id_data and id_data.get("del_flag") is None:
                reply_list = [{"id": x["_id"],
                               "author": x["author"],
                               "text": x["text"],
                               "date": x["date"],
                               "pict": x["pict"],
                               "reply": x["reply"],
                               "del_flag": x["del_flag"]
                               } for x in db.find_post(search_id)]
            else:
                abort(404)
        else:
            abort(405)
    except Exception as e:
        print(e)
        abort(404)

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
            flash("ログインをしてから投稿してください。")
    else:
        abort(405)

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
    else:
        abort(405)

    return redirect(url_for("details", post_data=req.getlist("reply")[0]))


@app.route("/del_post", methods=["POST"])
def del_form():
    if request.method == "POST":
        req = request.form
        db.delete_post(req.getlist("id")[0], current_user.id)
    else:
        abort(405)

    return redirect(url_for("index"))


@app.route("/login_form", methods=["POST"])
def login_form():
    if request.method == "POST":
        crypt = Bcrypt(app)
        try:
            user = User(request.form["account"])
            if user.info is not None and crypt.check_password_hash(user.info["Password"], request.form["password"]):
                login_user(user)
            else:
                flash("login failed")
        except Exception as e:
            print(e)
            flash("error check password. use password is old?")
    else:
        abort(405)

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
    else:
        abort(405)

    return redirect(url_for("index"))


@app.route("/delete_account", methods=["POST"])
def delete_account():
    if request.method == "POST":
        del_account = current_user.id
        logout_user()
        result = account_db.delete_account(del_account)
        flash(result)
    else:
        abort(405)
    return redirect(url_for("index"))


@app.route("/logout_form", methods=["POST"])
def logout_form():
    if request.method == "POST":
        logout_user()
    else:
        abort(405)

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
    suffix = ["png", "jpg", "bmp", "gif"]
    pict_suffix = picture.filename.split(".")[-1]
    try:
        if pict_suffix in suffix:
            return base64.b64encode(picture.read()).decode('utf8')
    except Exception as e:
        print(e)
    return None


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(Path(app.root_path, "cache", "favicon.png"), filename="favicon.png")


if __name__ == "__main__":
    app.run(debug=True)

