import helper_functions as hf
from flask import Flask, render_template, request, redirect, url_for


# Init
server = Flask(__name__, template_folder="templates")

udb = hf.Generate_db_user("Data/test.db")
adb = hf.Generate_db_admin("Data/test_ad.db")

udb.close_connection()
adb.close_connection()

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


@server.route('/admin_generate_new_user', methods=['GET', 'POST'])
def admin_new_user():
    if request.method == 'GET':
        return render_template('admin_newuser.html')
    else:
        udb = hf.Generate_db_user("Data/test.db")
        token = udb.add_user(dict(request.form))
        udb.close_connection()
        return render_template('user_generated.html',
                               uuid=token,
                               user=dict(request.form))


@server.route('/admin_userdatabase')
def admin_allusers():
    udb = hf.Generate_db_user("Data/test.db")
    users = udb.get_all_users()
    print(users)
    udb.close_connection()
    return render_template('table.html', data=users)


@server.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        udb = hf.Generate_db_user("Data/test.db")
        usertoken = dict(request.form)['token']
        check, uid = udb.check_user(usertoken)
        if check:
            udb.close_connection()
            return input_form(usertoken)
        else:
            udb.close_connection()
            return render_template('usernotfound.html', uuid=usertoken)


@server.route('/userform', methods=['GET', 'POST'])
def input_form(usertoken):
    if request.method == 'GET':
        return render_template('user_data.html', uuid=usertoken)
    else:
        data = dict(request.form)
        udb = hf.Generate_db_user("Data/test.db")
        udb.complete_user(data, usertoken)
        return render_template('success.html')

server.run("0.0.0.0", "5005")
