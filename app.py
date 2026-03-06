import os
import csv
from io import StringIO

from flask import Flask, render_template, request, redirect, jsonify, Response
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt

# ================= SAFE INIT =================

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET")

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# ================= IMPORT AFTER APP INIT =================

from auth.auth_routes import auth_bp
from auth.user_model import User

import modules.airdrop as airdrop
import modules.address as address
import modules.akun as akun

from web3_utils import get_balance

# register blueprint
app.register_blueprint(auth_bp)

# ================= USER LOADER =================

@login_manager.user_loader
def load_user(user_id):

    try:
        return User.get(user_id)
    except Exception:
        return None


# ==================================================
# LANDING PAGE
# ==================================================

@app.route("/")
def home():

    if current_user.is_authenticated:
        return redirect("/dashboard")

    return render_template("home.html")


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    data = airdrop.get_all(current_user.id)

    total = len(data)
    done_count = sum(
        1 for d in data if d.get("status") == "done"
    )

    pending = total - done_count

    return render_template(
        "dashboard.html",
        data=data,
        total=total,
        done=done_count,
        pending=pending
    )


# ==================================================
# AIRDROP ROUTES
# ==================================================

@app.route("/add_airdrop", methods=["POST"])
@login_required
def add_airdrop():

    airdrop.add(request.form, current_user.id)

    return redirect("/dashboard")


@app.route("/delete_airdrop/<id>")
@login_required
def delete_airdrop(id):

    airdrop.delete(id, current_user.id)

    return redirect("/dashboard")


@app.route("/done_airdrop/<id>")
@login_required
def done_airdrop(id):

    airdrop.done(id, current_user.id)

    return redirect("/dashboard")


@app.route("/edit_airdrop/<id>")
@login_required
def edit_airdrop(id):

    item = airdrop.get_by_id(id, current_user.id)

    if not item:
        return redirect("/dashboard")

    return render_template(
        "edit_airdrop.html",
        item=item
    )


@app.route("/update_airdrop/<id>", methods=["POST"])
@login_required
def update_airdrop(id):

    airdrop.update(id, request.form, current_user.id)

    return redirect("/dashboard")


# ==================================================
# SEARCH AIRDROP
# ==================================================

@app.route("/search_airdrop")
@login_required
def search_airdrop():

    q = request.args.get("q", "").lower()

    data = airdrop.get_all(current_user.id)

    results = [

        d for d in data

        if q in d.get("name", "").lower()
        or q in d.get("chain", "").lower()
        or q in d.get("type", "").lower()

    ]

    return jsonify(results)


# ==================================================
# EXPORT AIRDROP CSV
# ==================================================

@app.route("/export_airdrop")
@login_required
def export_airdrop():

    data = airdrop.get_all(current_user.id)

    if not data:
        return redirect("/dashboard")

    si = StringIO()
    cw = csv.writer(si)

    cw.writerow(data[0].keys())

    for row in data:
        cw.writerow(row.values())

    return Response(

        si.getvalue(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=airdrop.csv"
        }

    )


# ==================================================
# ADDRESS MANAGER
# ==================================================

@app.route("/address")
@login_required
def address_page():

    data = address.get_all(current_user.id)

    return render_template(
        "address.html",
        data=data
    )


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

    if not item:
        return redirect("/address")

    return render_template(
        "edit_address.html",
        item=item
    )


@app.route("/update_address/<id>", methods=["POST"])
@login_required
def update_address(id):

    address.update(id, request.form, current_user.id)

    return redirect("/address")


# ==================================================
# AKUN MANAGER
# ==================================================

@app.route("/akun")
@login_required
def akun_page():

    data = akun.get_all(current_user.id)

    return render_template(
        "akun.html",
        data=data
    )


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

    if not item:
        return redirect("/akun")

    return render_template(
        "edit_akun.html",
        item=item
    )


@app.route("/update_akun/<id>", methods=["POST"])
@login_required
def update_akun(id):

    akun.update(id, request.form, current_user.id)

    return redirect("/akun")


# ==================================================
# WEB3 WALLET SCANNER
# ==================================================

@app.route("/scan/<wallet>")
@login_required
def scan_wallet(wallet):

    try:

        balance = get_balance(wallet)

        return jsonify({
            "balance": balance
        })

    except Exception:

        return jsonify({
            "balance": "0"
        })


# ==================================================
# LOCAL RUN
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )