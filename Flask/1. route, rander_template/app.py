from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    List = [
        'section 1',
        'section 2',
        'section 3'
    ]
    return render_template('index.html', data = List)
if __name__ == '__main__':
    app.run(debug=True, port=3000)

