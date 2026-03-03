from flask import Flask, render_template, request, redirect, jsonify, Response
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from io import StringIO
import csv
import os

# ================= DATABASE =================
from database.init_db import init_db

# ================= AUTH =================
from auth.auth_routes import auth_bp
from auth.user_model import User

# ================= MODULES =================
import modules.airdrop as airdrop
import modules.address as address
import modules.akun as akun

# ================= WEB3 =================
from web3_utils import get_balance

# ==================================================
# INIT APP
# ==================================================

app = Flask(__name__)

# Gunakan ENV kalau nanti deploy
app.secret_key = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET")

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Init Database
init_db()

# ==================================================
# DASHBOARD AIRDROP
# ==================================================

@app.route("/")
@login_required
def dashboard():
    data = airdrop.get_all(current_user.id)

    total = len(data)
    done_count = sum(1 for d in data if d["status"] == "done")
    pending = total - done_count

    return render_template(
        "dashboard.html",
        data=data,
        total=total,
        done=done_count,
        pending=pending
    )


@app.route("/add_airdrop", methods=["POST"])
@login_required
def add_airdrop():
    airdrop.add(request.form, current_user.id)
    return redirect("/")


@app.route("/delete_airdrop/<id>")
@login_required
def delete_airdrop(id):
    airdrop.delete(id, current_user.id)
    return redirect("/")


@app.route("/done_airdrop/<id>")
@login_required
def done_airdrop(id):
    airdrop.done(id, current_user.id)
    return redirect("/")


@app.route("/edit_airdrop/<id>")
@login_required
def edit_airdrop(id):
    item = airdrop.get_by_id(id, current_user.id)
    return render_template("edit_airdrop.html", item=item)


@app.route("/update_airdrop/<id>", methods=["POST"])
@login_required
def update_airdrop(id):
    airdrop.update(id, request.form, current_user.id)
    return redirect("/")


# ================= SEARCH =================

@app.route("/search_airdrop")
@login_required
def search_airdrop():
    q = request.args.get("q", "").lower()
    data = airdrop.get_all(current_user.id)

    results = [
        d for d in data
        if q in d["name"].lower()
        or q in d["chain"].lower()
        or q in d["type"].lower()
    ]

    return jsonify(results)


# ================= EXPORT CSV =================

@app.route("/export_airdrop")
@login_required
def export_airdrop():
    data = airdrop.get_all(current_user.id)

    if not data:
        return redirect("/")

    si = StringIO()
    cw = csv.writer(si)

    cw.writerow(data[0].keys())
    for row in data:
        cw.writerow(row.values())

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=airdrop.csv"}
    )

# ==================================================
# ADDRESS
# ==================================================

@app.route("/address")
@login_required
def address_page():
    data = address.get_all(current_user.id)
    return render_template("address.html", data=data)


@app.route("/add_address", methods=["POST"])
@login_required
def add_address():
    address.add(request.form, current_user.id)
    return redirect("/address")


@app.route("/delete_address/<id>")
@login_required
def delete_address(id):
    address.delete(id, current_user.id)
    return redirect("/address")


@app.route("/edit_address/<id>")
@login_required
def edit_address(id):
    item = address.get_by_id(id, current_user.id)
    return render_template("edit_address.html", item=item)


@app.route("/update_address/<id>", methods=["POST"])
@login_required
def update_address(id):
    address.update(id, request.form, current_user.id)
    return redirect("/address")


# ================= WEB3 SCAN =================

@app.route("/scan/<wallet>")
@login_required
def scan_wallet(wallet):
    balance = get_balance(wallet)
    return jsonify({"balance": balance})


# ==================================================
# AKUN
# ==================================================

@app.route("/akun")
@login_required
def akun_page():
    data = akun.get_all(current_user.id)
    return render_template("akun.html", data=data)


@app.route("/add_akun", methods=["POST"])
@login_required
def add_akun():
    akun.add(request.form, current_user.id)
    return redirect("/akun")


@app.route("/delete_akun/<id>")
@login_required
def delete_akun(id):
    akun.delete(id, current_user.id)
    return redirect("/akun")


@app.route("/edit_akun/<id>")
@login_required
def edit_akun(id):
    item = akun.get_by_id(id, current_user.id)
    return render_template("edit_akun.html", item=item)


@app.route("/update_akun/<id>", methods=["POST"])
@login_required
def update_akun(id):
    akun.update(id, request.form, current_user.id)
    return redirect("/akun")


# ==================================================
# RUN LOCAL ONLY
# ==================================================

if __name__ == "__main__":
    app.run()