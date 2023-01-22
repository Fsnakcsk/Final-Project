from flask import Flask, flash, redirect, render_template, request, url_for
import sqlite3
from flask import _app_ctx_stack

#--------------------------------------
# DB
DATABASE = '/path/to/database.db'

app = Flask(__name__)

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(DATABASE)
    return top.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

#--------------------------------------

@app.route('/')
def zhong():
    return render_template('zhongtest.html')

if __name__ == "__main__":
    app.run(debug=True)