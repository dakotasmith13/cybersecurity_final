"""
CashCab's Secret Safe
Flask Routes

"""

from hash_pws import authenticate
import database
import secrets
import string

from config import display
from flask import Flask, render_template, request, url_for, flash, redirect, session
from hash_pws import hash_pw

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')


# Set maximum number of attempts to log in
MAX_ATTEMPTS = 3
# Special characters to test password strength
SPECIAL_CHAR = "!@#$%^&*{('.~`"
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 50


@app.route("/", methods=['GET', 'POST'])
def login():
    """Login the user. TODO """

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if 'counter' not in session:
            session['counter'] = 0
        # while session.get('counter') < MAX_ATTEMPTS:
        try:
            stored_password = database.get_user(username)
            if stored_password == 0:
                flash('Username does not exist', 'alert-danger')
                return render_template('login.html',
                                       title="Secure Login",
                                       heading="Secure Login")
            if authenticate(stored_password, password, 40):
                database.set_current_user(username)
                return redirect(url_for('logged_in'))
            else:
                session['counter'] = session.get('counter') + 1
                flash(f"Invalid username or password! You have {3 - session.get('counter')} attempts remaining", 'alert-danger')
                if session.get('counter') < MAX_ATTEMPTS:
                    return render_template('login.html',
                                           title="Secure Login",
                                           heading="Secure Login")
                else:
                    session.pop('counter', None)
                    return render_template('login_fail.html',
                                           title="Locked out",
                                           heading="Too many failed attempts")
        except KeyError:
            pass
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/home", methods=['GET', 'POST'])
def logged_in():
    """Home page after login"""
    flash(f"Welcome, {database.is_current_user()}! You have logged in!", 'alert-success')
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display)


@app.route("/logged-out", methods=['GET', 'POST'])
def log_out():
    """ Log out removes current user and then
    redirects to login page """

    flash("Successfully logged out.", 'alert-success')
    user = database.is_current_user()
    # make user not current user
    database.set_not_current_user(user)
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/accounting", methods=['GET', 'POST'])
def accounting():
    """Accounting Page"""

    # get user access level to determine whether they have access
    user = database.is_current_user()
    access_level = database.get_access_level(user)

    if access_level == 'accounting':
        flash("Successfully entered Accounting", 'alert-success')
        return render_template('accounting.html',
                               title="Accounting Page",
                               heading="Welcome to Accounting",
                               show=display)
    else:
        flash("You do not have access to accounting", 'alert-danger')
        return render_template('home.html',
                               title="Home Page",
                               heading="Home Page",
                               show=display)


@app.route("/it_helpdesk", methods=['GET', 'POST'])
def it_helpdesk():
    """IT helpdesk page"""

    flash("Successfully entered the IT Helpdesk", 'alert-success')
    return render_template('it_helpdesk.html',
                           title="IT Helpdesk Page",
                           heading="Welcome to the IT Helpdesk",
                           show=display)


@app.route("/engineering", methods=['GET', 'POST'])
def engineering():
    """Engineering page after login"""

    # get user access level to determine whether they have access
    user = database.is_current_user()
    access_level = database.get_access_level(user)
    if access_level == 'engineering':
        flash("Successfully logged in to engineering.", 'alert-success')
        return render_template('engineering_docs.html',
                               title="Engineering Page",
                               heading="Welcome to Engineering",
                               show=display)
    else:
        flash("You do not have access to engineering", 'alert-danger')
        return render_template('home.html',
                               title="Home Page",
                               heading="Home Page",
                               show=display)


@app.route("/time-reporting", methods=['GET'])
def time_reporting():
    """Time reporting page after login"""

    flash("Successfully entered Time Reporting", 'alert-success')
    return render_template('time-reporting.html',
                           title="Time Reporting Page",
                           heading="Welcome to Time Reporting",
                           show=display)


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    """Create account page"""

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            # if username already exists
            if database.is_user(username):
                flash("Username already taken, please try again", 'alert-danger')
            # if everything looks good
            elif not database.is_user(username) and password_strength(password):
                database.add_user(username, hash_pw(password), "engineering")
                flash("Successfully created account. Redirecting to login...", 'alert-success')
                return redirect(url_for('login'))
            # if password doesn't meet strength requirements
            elif not password_strength(password):
                flash("Password too weak. Please include one special character and a length of >8 and <25", 'alert'
                                                                                                            '-danger')

        except KeyError:
            pass
            flash("Invalid username or password!", 'alert-danger')
    return render_template('create_account.html',
                           password=generate_pass(),
                           title="Create Account Page",
                           heading="Create an Account")


def generate_pass():
    """
    Will generate random password for user
    :return: str with random pass
    """
    # will create string with letters, digits, and special chars
    pass_length = 12
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars
    # goes through string and creates random pw
    password = ''
    for _ in range(pass_length):
        password += ''.join(secrets.choice(alphabet))
    return password


def password_strength(test_password) -> bool:
    """
    Check basic password strength. Return true if password
    meets minimum complexity criteria, false otherwise.

    :param test_password: str
    :return: bool
    """
    if test_password.isalnum() or test_password.isalpha():
        return False
    if len(test_password) < PASSWORD_MIN_LENGTH:
        return False
    if len(test_password) > PASSWORD_MAX_LENGTH:
        return False
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in test_password:
        if ch in SPECIAL_CHAR:
            special_char_check = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        return False
    else:
        return True

