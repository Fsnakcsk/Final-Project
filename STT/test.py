from flask import Flask, flash, redirect, render_template, request, url_for
import sqlite3
from flask import _app_ctx_stack

import base64
import requests
from time import sleep

import urllib3
import json


app = Flask(__name__)

#======================================
#                 DB
#======================================

# DATABASE = '/path/to/database.db'

# app = Flask(__name__)

# def get_db():
#     top = _app_ctx_stack.top
#     if not hasattr(top, 'sqlite_db'):
#         top.sqlite_db = sqlite3.connect(DATABASE)
#     return top.sqlite_db

# @app.teardown_appcontext
# def close_connection(exception):
#     top = _app_ctx_stack.top
#     if hasattr(top, 'sqlite_db'):
#         top.sqlite_db.close()

#--------------------------------------

@app.route('/')
def Sound():
    dic = {'1' : "안녕하세요. 오늘도 멋진 하루 되세요"}
    return render_template('zhongtest.html', target=dic['1'])

@app.route('/STT', methods=['POST', 'GET'])
def STT():
    String_sound = ''
    String_target = ''
    
    sleep(6)
    count = 1
    
    #---------------------------------------------------------------------------
    #      AI API.DATA
    #---------------------------------------------------------------------------
    if request.method == 'POST':
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a" 
        if count == 1 :
            print(count)
            audioFilePath = "C:/Users/userpc/Desktop/정답2.wav"
        else :
            audioFilePath = "C:/Users/userpc/Desktop/정답"+ str(count) +".wav"
            count += 1
            print(count)
            
        languageCode = "korean"
        
        file = open(audioFilePath, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()
        
        requestJson = {    
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
        "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization": accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print("===== 결과 확인 ====")

        string = str(response.data,"utf-8")
        List = string.split('"')
        print(List)
        
        target = List[-2]
        target = target[:-1]
        
        
        dic = {'1' : "안녕하세요. 오늘도 멋진 하루 되세요"}
        String_sound = target
        String_target = target=dic['1']
        
        print(target)
        
        #---------------------------------------------------------------------------
        #       유사도 검사
        #---------------------------------------------------------------------------
        
        openApiURL = "http://aiopen.etri.re.kr:8000/ParaphraseQA"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a"
        sentence1 = String_sound
        sentence2 = String_target
        
        requestJson = {
        "argument": {
            "sentence1": sentence1 ,
            "sentence2": sentence2
            }
        }
        
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8","Authorization" :  accessKey},
            body=json.dumps(requestJson)
        )
        
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        print(str(response.data,"utf-8"))
        
        #--------------------------------------------------------------------------
        
        String = ''
        if target == dic['1'] :
            String += '맞췄습니다'
        else:
            String += '틀렸씁니다.'
            
        return render_template('zhongtest.html', target=dic['1'], sound = target, ck=String)
    
        
          
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user+' by Get'))
    

if __name__ == "__main__":
    app.run(debug=True)