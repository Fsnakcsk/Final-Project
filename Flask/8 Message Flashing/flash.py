# API 확인
# https://flask.palletsprojects.com/en/2.0.x/api/#message-flashing
# https://pythonise.com/series/learning-flask/flask-message-flashing

from flask import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import pandas as pd
import numpy as np
import os

from selenium.webdriver.common.keys import Keys

import warnings
warnings.filterwarnings('ignore')






app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
           request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('성공적으로 로그인되었습니다!')
            return redirect(url_for('index'))

    


---
    name=['LG 에어로타워']
    category=['별점']

    #LG 에어로타워 후기
    ns_address="https://search.shopping.naver.com/catalog/30128278618?cat_id=50002543&frm=NVSCPRO&query=%EC%97%90%EC%96%B4%EB%A1%9C%ED%83%80%EC%9B%8C&NaPm=ct%3Dl0ksn0vc%7Cci%3D5bbd25c0299ce5dbcb72ff2b1d41488ebd6d52ce%7Ctr%3Dsls%7Csn%3D95694%7Chk%3D87194ce8ced4cb2b52968022b8eb9db67602d12e"


    #xpath
    #shoppingmall_review ="/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/ul"
    #shoppingmall_review = "/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/ul/li[1]/div[3]/a"
    # shoppingmall_review = "/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/ul/li[1]/div[2]/div[1]""

    shoppingmall_review = "/html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div[2]/ul/li[5]/a/strong"
    # /html/body/div/div/div[2]/div[2]/div[2]/div[3]/div[6]/ul/li[1]/div[2]/div[1]/p

    return render_template('login.html', error=error
                                        , bcd = shoppingmall_review)

if __name__ == "__main__":
    app.run(debug=True)