from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
import sqlite3 as sql
from flask import g

import base64
import requests
from time import sleep

import urllib3
import json


app = Flask(__name__)

#======================================
#                 DB
#======================================

#                              고칠 부분
DATABASE_URI = 'C:\\Users\\userpc\\Desktop\\Github Profile\\Final-Project\\STT\\sttdb.db'

# conn = sql.connect('sttdb.db', isolation_level=None)
# cur = conn.cursor()
# cur.execute(
#     'CREATE TABLE IF NOT EXISTS STT (id TEXT, p TEXT, url TEXT)')
# cur.close()


# id = 1
# p = "안녕하세요. 오늘도 멋진 하루 되세요"
# url = 'C:\\Users\\userpc\\Desktop\\정답1.wav'

# conn = sql.connect(DATABASE_URI, isolation_level=None)
# cur = conn.cursor()
# cur.execute("""INSERT INTO STT(id, p, url) 
#                     VALUES(?, ?, ?)""", (id, p, url))
# conn.commit()
# cur.close()

conn = sql.connect(DATABASE_URI, isolation_level=None)
cur = conn.cursor()

cur.execute("SELECT * FROM STT")
db_text = str(cur.fetchmany(size=1))
print(db_text)

db_List = db_text.split("'")
sound_url = db_List[5]
sound_target = db_List[3]


#-------------------------------------------------------------
#      main
#-------------------------------------------------------------
@app.route('/')
def Sound():
    dic = {'1' : sound_target}
    return render_template('zhongtest.html', target=dic['1'])

@app.route('/STT', methods=['POST', 'GET'])
def STT():
    
    String_sound = ''
    String_target = ''
    
    sleep(5)
    count = 1
    
    #---------------------------------------------------------------------------
    #      STT Open API
    #---------------------------------------------------------------------------
    if request.method == 'POST':
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
        accessKey = "f0f9fd15-daef-4655-b516-d7a9711c696a" 
        if count == 1 :
            print(count)
            audioFilePath = "C:/Users/userpc/Desktop/정답1.wav"
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
        #       유사도 검사 NLP Open API
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

        NLP_String = str(response.data,"utf-8")
        NLP_List = NLP_String.split('"')
        print(NLP_List)
        
        NLP_reuslt = NLP_List[-2]
        # NLP_reuslt = NLP_target[:-1]
        print(NLP_reuslt)
        
        #--------------------------------------------------------------------------
        #     검증 결과 추출 및 전송
        #--------------------------------------------------------------------------
        
        String = ''
        if NLP_reuslt == 'paraphrase' :
            String += '유사합니다'
        else:
            String += '유사하지 않습니다'
        #                                             정답문장          TTS        체크 결과
        return render_template('zhongtest.html', target=dic['1'], sound = target, ck=String)


if __name__ == "__main__":
    app.run(debug=True)