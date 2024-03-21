#blueprints/auth.py
from flask import Flask, render_template, request, url_for, redirect, flash,Blueprint

#wtf forms import
from forms import LoginForm, RegistrationForm

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db,Chef

auth_bp = Blueprint('auth', __name__)

# Create your login manager
login_manager = LoginManager()

# Initialize the login manager with the blueprint
login_manager.init_app(auth_bp)

#LOGIN MANAGER
@login_manager.user_loader
def load_user(user_id):
  return db.session.get(Chef, int(user_id))


#LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    title = "Chez Chef"
    # Override next on query string to display warning
    next_url = request.args.get('next')
    if next_url:
        flash('Please log in to access this page.', 'warning')

    form = LoginForm()
    if form.validate_on_submit():
        chef = Chef.query.filter_by(email=form.email.data).first()
        if chef and chef.check_password(form.password.data):
            login_user(chef)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login or password incorrect', 'error')

    #form did NOT validate
    if request.method == 'POST' and not form.validate():
          for field, errors in form.errors.items():
              for error in errors:
                  flash(f"Error in {field}: {error}", 'error')
    context = {
        "title": title,
        "form": form
    }
    return render_template('login.html',**context)

#LOGOUT
@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout Successful!', 'success')
    return redirect(url_for('index'))

#SIGN_UP
@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    title = "Chez Chef"
    form = RegistrationForm()
    if form.validate_on_submit():
        chef= Chef(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email=form.email.data)
        chef.set_password(form.password.data)
        db.session.add(chef)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    #form did NOT validate
    if request.method == 'POST' and not form.validate():
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')

    context = {
        "title": title,
        "form": form
    }
    return render_template('sign_up.html', **context)
