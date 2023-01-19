from flask import Flask, flash, redirect, render_template, request, url_for



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/STT', methods=['GET', 'POST'])
def STT():


if __name__ == "__main__":
    app.run(debug=True)