from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'

    
@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name=user+' by Get'))


if __name__ == '__main__':
    app.run(debug=True)