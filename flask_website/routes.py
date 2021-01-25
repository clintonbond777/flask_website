import os
import re
import secrets



from flask import flash, redirect, render_template, request, url_for, jsonify, abort, session
from flask_login import current_user, login_required, login_user, logout_user
from PIL import Image

import plotly
import plotly.graph_objs as go 
import numpy as np
import json
import pandas as pd

from flask_website import app, bcrypt, db
from flask_website.forms import (
    LoginForm,
    CreateProgramForm,
    CreateProjectForm,
    CreateCaseForm,
    CreateModelForm,
    RegistrationForm,
    UpdateAccountForm
)
from flask_website.models import Case, Program, Project, User, Model


@app.route("/plot")
def plot():
    bar = create_plot('blargh')
    print(Program.query.all())
    return render_template("plot.html", plot = bar)

def create_plot(feature):
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



@app.route("/")
@app.route("/home")
def home():
    print(Program.query.all())
    return render_template("home.html", programs=Program.query.all())


@app.route("/about/")
def about():
    return render_template("home.html")


@app.route("/register/", methods=["GET", "POST"])
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


@app.route("/login/", methods=["GET", "POST"])
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


@app.route("/logout/")
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


@app.route("/account/", methods=["GET", "POST"])
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


@app.route("/newprogram/", methods=["GET", "POST"])
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


@app.route("/program/<int:program_id>/")
@login_required
def program(program_id):
    program = Program.query.get_or_404(program_id)
    projects = program.project
    return render_template(
        "program.html", title=program.name, program=program, projects=projects
    )


@login_required
@app.route("/program/<int:program_id>/update/", methods=["GET", "POST"])
def update_program(program_id):
    program = Program.query.get_or_404(program_id)

    form = CreateProgramForm()

    if form.validate_on_submit():
        program.name = form.name.data
        program.description = form.description.data
        db.session.commit()
        flash("Your Program has been updated")
        return redirect(url_for("program", program_id=program_id))

    elif request.method == "GET":
        form.name.data = program.name
        form.description.data = program.description
        return render_template(
            "create_program.html",
            title="Edit a Program",
            form=form,
            legend="Update Program",
        )


@app.route("/newproject/", methods=["GET", "POST"])
@login_required
def newproject():
    form = CreateProjectForm()
    if form.validate_on_submit():
        flash("Your Project has been created")
        project = Project(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
            program_id=form.program_select.data
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("create_project.html", title="Create a Project", form=form)


@login_required
@app.route("/project/<int:project_id>/")
def project(project_id):

    project = Project.query.get_or_404(project_id)
    program = Program.query.get_or_404(project.program_id)

    cases = project.case
    return render_template(
        "project.html",
        title=program.name,
        program=program,
        project=project,
        cases=cases,
    )


@login_required
@app.route("/project/<int:project_id>/update/", methods=["GET", "POST"])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    # program_id_inter = project.program_id
    # if project.creator != current_user:
    # abort(403)

    form = CreateProjectForm()

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash("Your Project has been updated")
        return redirect(url_for("project", project_id=project.id))
        
    elif request.method == "GET":
        form.name.data = project.name
        form.description.data = project.description
        return render_template("create_project.html", title="Edit a Project", form=form)

    return render_template(
        "create_program.html",
        title="Create a Program",
        form=form,
        legend="Update Program",
    )


@login_required
@app.route("/<int:program_id>/<int:project_id>/<int:case_id>/")
def case(program_id, project_id, case_id):
    program = Program.query.get_or_404(program_id)
    project = Project.query.get_or_404(project_id)
    cases = project.case
    return render_template(
        "case.html", title=program.name, program=program, project=project, case=cases
    )


@app.route("/newcase/", methods=["GET", "POST"])
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
            #session['new_case'] =  dict([(desc, field) for desc, field in form.data.items()])
        )
        return redirect(url_for('newmodel'))


@app.route("/newmodel/", methods=["GET", "POST"])
@login_required
def newmodel():
    program = Program.query.all()
    form = CreateModelForm()
    if request.method == "GET":
        return render_template("create_model.html", form=form)

    if form.validate_on_submit():  # and request.form["form_name"] == "PickProject":
        
        model = Model(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id,
            program_id=form.program_select.data
        )
        db.session.add(model)
        db.session.flush()
        db.session.commit()

        case = Case(name = session['newcase']['name'],
        description = session['newcase']['description'], 
        created_by = current_user.id,
        project_id = session['newcase']['project_select'],
        model_id = model.id,
        baseline_id = 1,
        ridemap_id = 1
        )
        db.session.add(model)
        db.session.commit()
        return redirect(url_for("home"))


@app.route("/_get_program_info/")
def _get_program_info():
    print(request.args)
    program_ID = request.args.get("program_select_var", "default_if_none")
    print(program_ID)

    output = {}
    output["project"] = [
        (x.id, x.name) for x in Project.query.filter_by(program_id=program_ID)
    ]
    output["geometry"] = [(x.id, x.name) for x in Model.query.filter_by(program_id=program_ID)]
    return jsonify(output)