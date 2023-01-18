from flask import *
app = Flask(__name__)
app.secret_key = "amustring"


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login2.html")


@app.route('/success', methods=["POST"])
def success():
    if request.method == "POST":
        session['email'] = request.form['email']
    return render_template('success.html')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)  # pop 메소드로 세션 변수 제거
        return render_template('logout.html')
    else:
        return '<p>user already logged out</p>'


@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        return render_template('profile.html', name=email)
    else:
        return '<p>Please login first</p>'


if __name__ == '__main__':
    app.run(debug=True)