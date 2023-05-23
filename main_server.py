import sqlite3
from flask import Flask, render_template, redirect, url_for


# Init
server = Flask(__name__, template_folder="templates")

db = sqlite3.connect()

@server.route('/')
def start():
    return render_template('index.html')


@server.route('/userform', methods=['GET', 'POST'])
def input_form():
    return render_template('input_mask.html')


server.run("0.0.0.0", "5005")
