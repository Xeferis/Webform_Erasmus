import helper_functions as hf
from flask import Flask, render_template, request, redirect, abort, session


# Init
server = Flask(__name__, template_folder="templates")

server.secret_key = b'd1d1s#s<r7k3y'

udb = hf.Generate_db_user("Data/test.db")
adb = hf.Generate_db_admin("Data/test_ad.db")

udb.close_connection()
adb.close_connection()


@server.route('/')
def start():
    return render_template('index.html')


@server.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        if session:
            return render_template('admin.html', username=session['username'])
        return render_template('login.html')
    elif request.method == 'POST':
        adb = hf.Generate_db_admin("Data/test_ad.db")
        in_data = dict(request.form)
        a_data = adb.get_admin(in_data['email'])
        adb.close_connection()
        if a_data[0][-1] == in_data['password']:
            session['username'] = a_data[0][1]
            in_data = None
            a_data = None
            return redirect('admin_dashboard')
        else:
            in_data = None
            a_data = None
            return render_template("failed_login.html")
    else:
        return render_template('404.html')


@server.route('/admin_logout')
def admin_logout():
    session.pop('username', None)
    return redirect('/')


@server.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        in_data = dict(request.form)
        adb = hf.Generate_db_admin("Data/test_ad.db")
        adb.add_admin(in_data)
        try:
            a_data = adb.get_admin(in_data['email'])
        except:
            a_data = None
            in_data = None
            return render_template('failed_login.html')
        a_data = None
        in_data = None
        return render_template('success.html')
    else:
        return render_template('404.html')


@server.route('/admin_newpassword', methods=['GET', 'POST'])
def admin_newpassword():
    return render_template('forgot-password.html')


@server.route('/admin_dashboard')
def admin_start():
    if session:
        return render_template('admin.html', username=session['username'])
    return redirect('admin_register')


@server.route('/admin_generate_new_user', methods=['GET', 'POST'])
def admin_new_user():
    if request.method == 'GET':
        if session:
            return render_template('admin_newuser.html', username=session['username'])
        return redirect('admin_register')
    else:
        udb = hf.Generate_db_user("Data/test.db")
        token = udb.add_user(dict(request.form))
        udb.close_connection()
        return render_template('user_generated.html',
                               uuid=token,
                               user=dict(request.form))


@server.route('/admin_userdatabase')
def admin_allusers():
    if session:
        udb = hf.Generate_db_user("Data/test.db")
        users = udb.get_all_users()
        print(users)
        udb.close_connection()
        return render_template('table.html', data=users)
    return redirect('admin_register')


@server.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        udb = hf.Generate_db_user("Data/test.db")
        global usertoken
        usertoken = dict(request.form)['token']
        check, uid = udb.check_user(usertoken)
        if check:
            udb.close_connection()
            return redirect('addinguser')
        else:
            udb.close_connection()
            return render_template('usernotfound.html', uuid=usertoken)


@server.route('/addinguser', methods=['GET', 'POST'])
def adding_user():
    if request.method == 'GET':
        global usertoken
        udb = hf.Generate_db_user("Data/test.db")
        data = udb.get_user(usertoken)
        data = data[0][2:]
        print(data)
        datalist = []
        disabledlist = []
        for specific in data:
            if specific is None:
                disabledlist.append('')
            else:
                datalist.append(specific)
                disabledlist.append('disabled')

        print(disabledlist)
        print(datalist)
        udb.close_connection()
        try:
            return render_template('user_data.html', uuid=usertoken, data=datalist, disopt=disabledlist)
        except:
            abort(404)
    else:
        data = dict(request.form)
        print(data)
        udb = hf.Generate_db_user("Data/test.db")
        udb.complete_user(data, usertoken)
        udb.close_connection()
        return render_template('success.html')


server.run("0.0.0.0", "5005")
