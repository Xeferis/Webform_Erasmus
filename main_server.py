import helper_functions as hf
from flask import Flask, render_template, redirect, url_for


# Init
server = Flask(__name__, template_folder="templates")

udb = hf.Generate_db_user("Data/test.db")
adb = hf.Generate_db_admin("Data/test_ad.db")


@server.route('/')
def start():
    return render_template('index.html')


@server.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    return render_template('login.html')


@server.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    return render_template('register.html')


@server.route('/admin_newpassword', methods=['GET', 'POST'])
def admin_newpassword():
    return render_template('forgot-password.html')


@server.route('/admin_dashboard')
def admin_start():
    return render_template('admin.html')


@server.route('/admin_userdatabase')
def admin_allusers():
    users = udb.content
    print(users)
    return render_template('table.html', data=users)


@server.route('/register', methods=['GET', 'POST'])
def register_user():
    return render_template('registration.html')


@server.route('/userform', methods=['GET', 'POST'])
def input_form():
    return render_template('user_data.html')


server.run("0.0.0.0", "5005")
