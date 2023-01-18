from flask import Flask, render_template

#from flask_bootstrap import Bootstrap4 # pip install flask-bootstrap
#bootstrap = Bootstrap4(app) # 将App 运用到 Bootstrap

app = Flask(__name__)

@app.route('/')
def index():
    List = [
        'section 1',
        'section 2',
        'section 3'
    ]
    return render_template('index.html',title = 'Home', data = List)


if __name__ == '__main__':
    app.run(debug=True, port=3000)

