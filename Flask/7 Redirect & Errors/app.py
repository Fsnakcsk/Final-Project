# https://www.tutorialspoint.com/flask/flask_redirect_and_errors.htm

from flask import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/auth', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['name'] == 'admin':
            return redirect(url_for('success')) #跳转到success
        

@app.route('/success')
def success():
    return 'logged in successfully 성공적으로 로그인했습니다'

if __name__ == '__main__':
    app.run(debug=True)