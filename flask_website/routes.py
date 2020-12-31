import os
import re
import secrets

from flask import flash, redirect, render_template, request, url_for, jsonify, abort
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

from flask_website import app, bcrypt, db
from flask_website.forms import (
    CreateProgramForm,
    CreateProjectForm,
    CreateCaseForm,
    LoginForm,
    RegistrationForm,
    UpdateAccountForm,
)
from flask_website.models import Case, Program, Project, User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", programs=Program.query.all())


@app.route("/about")
def about():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash(
            f"Account created for {form.username.data}!. You are now able to login",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_sized = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_sized)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@app.route("/newprogram", methods=["GET", "POST"])
@login_required
def newprogram():
    form = CreateProgramForm()
    if form.validate_on_submit():
        flash("Your Program has been created")
        program = Program(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
        )
        db.session.add(program)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("create_program.html", title="Create a Program", form=form)


@app.route("/programs/<int:program_id>")
@login_required
def programs(program_id):
    program = Program.query.get_or_404(program_id)
    projects = program.project
    return render_template(
        "program.html", title=program.name, program=program, projects=projects
    )


@app.route("/programs/<int:program_id>/update")
@login_required
def update_program(program_id):
    program = Program.query.get_or_404(program_id)
    if program.creator != current_user:
        abort(403)

    form = CreateProgramForm()

    if form.validate_on_submit():
        program.name = form.name.data
        program.description = form.description.data
        db.session.commit()
        flash("Your Program has been updated")
    elif request.method == "GET":
        form.name.data = program.name
        form.description.data = program.description
        return redirect(url_for("programs", program_id=program.id))

    return render_template(
        "create_program.html",
        title="Create a Program",
        form=form,
        legend="Update Program",
    )


@app.route("/newproject", methods=["GET", "POST"])
@login_required
def newproject():
    form = CreateProjectForm()
    if form.validate_on_submit():
        flash("Your Project has been created")
        project = Project(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
            program_id=form.program_select.data,
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_project.html", title="Create a Project", form=form)


@login_required
@app.route("/programs/<int:program_id>/<int:project_id>/")
def project(program_id, project_id):
    program = Program.query.get_or_404(program_id)
    project = Project.query.get_or_404(project_id)
    cases = project.case
    return render_template(
        "project.html",
        title=program.name,
        program=program,
        project=project,
        cases=cases,
    )


@login_required
@app.route("/programs/<int:program_id>/<int:project_id>/<int:case_id>")
def case(program_id, project_id, case_id):
    program = Program.query.get_or_404(program_id)
    projects = Project.query.get_or_404(project_id)
    case = Case.query.get_or_404(case_id)
    return render_template(
        "case.html", title=program.name, program=program, projects=projects, case=case
    )


@app.route("/newcase", methods=["GET", "POST"])
@login_required
def newcase():
    program = Program.query.all()
    form = CreateCaseForm()
    form.program_select.choices = [(g.id, g.name) for g in Program.query.all()]
    form.project_select.choices = [(g.id, g.name) for g in Project.query.all()]
    if request.method == "GET":
        return render_template("create_case.html", form=form)

    if form.validate_on_submit():  # and request.form["form_name"] == "PickProject":
        # code to process form
        flash(
            "Program: %s, Project: %s"
            % (form.program_select.data, form.project_select.data)
        )
    return redirect(url_for("newcase"))


@app.route("/_get_project/")
def _get_project():
    # good for debug, make sure args were sent
    print(request.args)
    program_ID = request.args.get("program_select_var", "default_if_none")
    print(program_ID)

    output = {}
    # output["project"] = [
    #     ("1", "this is one"),
    #     ("2", "this is two"),
    #     ("3", "this is :)"),
    # ]

    output["project"] = [
        (x.id, x.name) for x in Project.query.filter_by(program_id=program_ID)
    ]
    print(output, "\n")
    #

    print(jsonify(output))
    return jsonify(output)