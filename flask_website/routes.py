from flask import render_template, url_for, flash, redirect, request
from flask_website.models import User, Program, Project
from flask_website.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateProgramForm, CreateProjectForm
from flask_website import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

@app.route("/")
@app.route("/home")
def home(): 
    return render_template('home.html', programs = Program.query.all())

@app.route("/about")
def about(): 
    return render_template('home.html')

@app.route("/register", methods = ['GET','POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!. You are now able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
    output_sized = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_sized)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods = ['GET', 'POST'])
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
        flash('your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)

@app.route("/newprogram", methods = ['GET', 'POST'])
def newprogram():
    form = CreateProgramForm()
    if form.validate_on_submit():
        flash('Your Program has been created')
        program = Program(name=form.name.data, description = form.description.data, created_by = current_user.id)
        db.session.add(program)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_program.html', title = 'Create a Program', form = form)


@app.route("/programs/<int:program_id>")
def program(program_id):
    program = Program.query.get_or_404(program_id)
    projects =program.project 
    return render_template('program.html', title = program.name, program = program, projects = projects)

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
        flash('Your Program has been updated')
    elif request.method == 'GET':
        form.name.data = program.name
        form.description.data = program.description
        return redirect (url_for ('program', program_id = program.id))
    return render_template('create_program.html', title = 'Create a Program', form = form, legend = 'Update Program')


@app.route("/newproject", methods=['GET', 'POST'])
def newproject():
    form = CreateProjectForm()
    if form.validate_on_submit():
        flash('Your Project has been created')
        project = Project(name = form.name.data, description = form.description.data, created_by = current_user.id, program_id = form.program_select.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_project.html', title = 'Create a Project', form = form)


@app.route("/programs/<int:program_id>/<int:project_id>/<int:case_id>")
def project(program_id,project_id):
    program = Program.query.get_or_404(program_id)
    projects =program.project
    
    return render_template('project.html', title = program.name, program = program, projects = projects)


@app.route("/programs/<int:program_id>/<int:project_id>/<int:case_id>")
def case(program_id,project_id, case_id):
    program = Program.query.get_or_404(program_id)
    projects =program.project
    case = Case.query.get_or_404(case_id)
    return render_template('case.html', title = program.name, program = program, projects = projects, case = case)