import datetime
import functools
import re
import secrets
from urllib.parse import quote

import markupsafe
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session

import config
import jobs
import users
import visits

app = Flask(__name__)
app.secret_key = config.secret_key
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

PER_PAGE = 20
MAX_TITLE = 100
MAX_ADDRESS = 200
MAX_DESCRIPTION = 5000
MAX_NOTES = 2000
MAX_PRICE = 1000000
MAX_WINDOWS = 5000

USERNAME_PATTERN = re.compile(r"^[a-z0-9_]{3,20}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def require_login():
    if "user_id" not in session:
        abort(403)


def login_required(view):
    """Send a visitor who is not logged in to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Kirjaudu sisään nähdäksesi sivun.")
            return redirect("/login")
        return view(**kwargs)

    return wrapped_view


def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.before_request
def prepare_session():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


@app.template_filter()
def show_price(price):
    return f"{price:,}".replace(",", " ") + " €"


@app.errorhandler(403)
def forbidden(_error):
    message = "Sinulla ei ole oikeutta tähän sivuun."
    return render_template("error.html", message=message), 403


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html",
                           message="Sivua ei löytynyt."), 404


def page_count(total):
    return max((total + PER_PAGE - 1) // PER_PAGE, 1)


def current_page():
    value = request.args.get("page", "1")
    if not value.isdigit():
        return 1
    return max(int(value), 1)


def read_job_form():
    values = {
        "title": request.form.get("title", "").strip(),
        "address": request.form.get("address", "").strip(),
        "description": request.form.get("description", "").strip(),
        "window_count": request.form.get("window_count", "").strip(),
        "price": request.form.get("price", "").strip(),
    }
    if not 3 <= len(values["title"]) <= MAX_TITLE:
        return None
    if not 3 <= len(values["address"]) <= MAX_ADDRESS:
        return None
    if len(values["description"]) > MAX_DESCRIPTION:
        return None
    if not values["window_count"].isdigit():
        return None
    if not values["price"].isdigit():
        return None
    values["window_count"] = int(values["window_count"])
    values["price"] = int(values["price"])
    if not 1 <= values["window_count"] <= MAX_WINDOWS:
        return None
    if not 0 <= values["price"] <= MAX_PRICE:
        return None

    values["class_ids"] = []
    for value in request.form.getlist("class_id"):
        if not value.isdigit():
            return None
        class_id = int(value)
        if not jobs.get_class(class_id):
            return None
        if class_id not in values["class_ids"]:
            values["class_ids"].append(class_id)
    if not values["class_ids"]:
        return None
    return values


@app.route("/")
@login_required
def index():
    page = current_page()
    total = jobs.count_jobs()
    job_list = jobs.get_jobs(page, PER_PAGE)
    return render_template("index.html", jobs=job_list, page=page,
                           pages=page_count(total), base_url="/?")


@app.route("/job/<int:job_id>")
@login_required
def show_job(job_id):
    job = jobs.get_job(job_id)
    if not job:
        abort(404)
    job_classes = jobs.get_job_classes(job_id)
    job_visits = visits.get_visits(job_id)
    is_owner = session.get("user_id") == job["user_id"]
    return render_template("show_job.html", job=job, classes=job_classes,
                           visits=job_visits, is_owner=is_owner,
                           today=datetime.date.today().isoformat())


@app.route("/find")
@login_required
def find_jobs():
    query_text = request.args.get("query", "").strip()[:100]
    class_value = request.args.get("class_id", "").strip()
    class_id = int(class_value) if class_value.isdigit() else None

    page = current_page()
    if query_text or class_id:
        results, total = jobs.find_jobs(query_text, class_id, page, PER_PAGE)
    else:
        results, total = [], 0
    base_url = "/find?query=" + quote(query_text) + "&class_id="
    base_url += str(class_id) if class_id else ""
    base_url += "&"
    return render_template("find_jobs.html", query=query_text,
                           class_id=class_id, classes=jobs.get_classes(),
                           results=results, page=page,
                           pages=page_count(total), base_url=base_url)


@app.route("/user/<int:user_id>")
@login_required
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    stats = users.get_stats(user_id)
    page = current_page()
    total = jobs.count_jobs_by_user(user_id)
    job_list = jobs.get_jobs_by_user(user_id, page, PER_PAGE)
    return render_template("show_user.html", user=user, stats=stats,
                           jobs=job_list, page=page, pages=page_count(total),
                           base_url="/user/" + str(user_id) + "?")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        check_csrf()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not USERNAME_PATTERN.match(username):
            flash("Tunnuksen tulee olla 3–20 merkkiä pitkä ja siinä voi "
                  "olla vain pieniä kirjaimia, numeroita ja alaviivoja.")
            return render_template("register.html", username=username)
        if not 8 <= len(password) <= 100:
            flash("Salasanan tulee olla 8–100 merkkiä pitkä.")
            return render_template("register.html", username=username)
        if users.get_user_by_name(username):
            flash("Tunnus on jo käytössä.")
            return render_template("register.html", username=username)

        users.create_user(username, password)
        flash("Tunnus luotu, voit kirjautua sisään.")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        check_csrf()
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user_id = users.check_login(username, password)
        if not user_id:
            flash("Väärä tunnus tai salasana.")
            return render_template("login.html", username=username)

        session["user_id"] = user_id
        session.pop("csrf_token", None)
        flash("Olet kirjautunut sisään.")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    check_csrf()
    session.pop("user_id", None)
    session.pop("csrf_token", None)
    flash("Olet kirjautunut ulos.")
    return redirect("/")


@app.route("/new_job", methods=["GET", "POST"])
@login_required
def new_job():
    if request.method == "GET":
        return render_template("new_job.html", classes=jobs.get_classes(),
                               values={}, selected=[])

    if request.method == "POST":
        check_csrf()
        values = read_job_form()
        if not values:
            flash("Tarkista lomakkeen tiedot ja valitse vähintään yksi "
                  "luokittelu.")
            return render_template("new_job.html", classes=jobs.get_classes(),
                                   values=request.form,
                                   selected=request.form.getlist("class_id"))

        job_id = jobs.add_job(values["title"], values["address"],
                              values["window_count"], values["price"],
                              values["description"], session["user_id"],
                              values["class_ids"])
        flash("Kohde lisätty.")
        return redirect("/job/" + str(job_id))

    return render_template("new_job.html", classes=jobs.get_classes(),
                           values={}, selected=[])


@app.route("/job/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    job = jobs.get_job(job_id)
    if not job:
        abort(404)
    if job["user_id"] != session["user_id"]:
        abort(403)

    job_classes = jobs.get_job_classes(job_id)
    selected = [str(item["id"]) for item in job_classes]

    if request.method == "GET":
        values = {"title": job["title"], "address": job["address"],
                  "window_count": job["window_count"], "price": job["price"],
                  "description": job["description"]}
        return render_template("edit_job.html", job=job,
                               classes=jobs.get_classes(), values=values,
                               selected=selected)

    if request.method == "POST":
        check_csrf()
        values = read_job_form()
        if not values:
            flash("Tarkista lomakkeen tiedot ja valitse vähintään yksi "
                  "luokittelu.")
            job = jobs.get_job(job_id)
            return render_template("edit_job.html", job=job,
                                   classes=jobs.get_classes(),
                                   values=request.form,
                                   selected=request.form.getlist("class_id"))

        jobs.update_job(job_id, values["title"], values["address"],
                        values["window_count"], values["price"],
                        values["description"], values["class_ids"])
        flash("Kohde päivitetty.")
        return redirect("/job/" + str(job_id))

    return redirect("/job/" + str(job_id))


@app.route("/job/<int:job_id>/remove", methods=["GET", "POST"])
@login_required
def remove_job(job_id):
    job = jobs.get_job(job_id)
    if not job:
        abort(404)
    if job["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_job.html", job=job)

    if request.method == "POST":
        check_csrf()
        jobs.remove_job(job_id)
        flash("Kohde poistettu.")
        return redirect("/")

    return redirect("/job/" + str(job_id))


@app.route("/job/<int:job_id>/visit", methods=["POST"])
def add_visit(job_id):
    require_login()
    check_csrf()
    job = jobs.get_job(job_id)
    if not job:
        abort(404)

    visit_date = request.form.get("visit_date", "").strip()
    notes = request.form.get("notes", "").strip()
    error = None
    if not DATE_PATTERN.match(visit_date):
        error = "Anna päivämäärä muodossa vvvv-kk-pp."
    else:
        try:
            datetime.date.fromisoformat(visit_date)
        except ValueError:
            error = "Päivämäärä ei ole kelvollinen."
    if not error and not 3 <= len(notes) <= MAX_NOTES:
        error = "Muistiinpanon tulee olla 3–2000 merkkiä pitkä."
    if error:
        flash(error)
        return redirect("/job/" + str(job_id))

    visits.add_visit(job_id, session["user_id"], visit_date, notes)
    flash("Käynti kirjattu.")
    return redirect("/job/" + str(job_id))


@app.route("/visit/<int:visit_id>/remove", methods=["POST"])
def remove_visit(visit_id):
    require_login()
    check_csrf()
    visit = visits.get_visit(visit_id)
    if not visit:
        abort(404)
    if visit["user_id"] != session["user_id"]:
        abort(403)

    visits.remove_visit(visit_id)
    flash("Käynti poistettu.")
    return redirect("/job/" + str(visit["job_id"]))


if __name__ == "__main__":
    app.run(port=5000)
