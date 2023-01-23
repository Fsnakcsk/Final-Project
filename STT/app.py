from flask import Flask, render_template, url_for, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def worng_test():
    if request.method == 'POST':
        text = request.form['나비']
        
        conn = sqlite3.connect('ijm.db', isolation_level=None)
        cursor = conn.cursor()
        param = text
        m = cursor.execute("SELECT * FROM wrong_test WHERE text = '%s'" % param)
        
        for x in m:
            rec_d1 = x[2] #right1
            rec_d2 = x[3] #right2
            rec_d3 = x[4] #right3
            rec_d4 = x[5] #wrong
            
        # root = 'C:\\Users\\admin\\Desktop\\최종 프로젝트\\틀린그림찾기\\'+ param
        # a = os.listdir(root)
        # a.write(rec_d4)
        
        with open('C:\\Users\\admin\\Desktop\\최종 프로젝트\\틀린그림찾기\\나비'+ text +'.png', 'wb') as f:
            f.write(rec_d4)
            
        conn.commit()
        cursor.close()
        conn.close()
        
        return render_template('show.html', text = text, d1 = rec_d1, d2 = rec_d2, d3 = rec_d3,d4 = rec_d4)



if __name__ == "__main__":
    app.run(debug = True)


