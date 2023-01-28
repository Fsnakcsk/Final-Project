from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/test', methods = ['POST'])
def test_api():
    return Response(json.dumps({'Message':'Hello World!'}), status = 200)



if __name__ == '__main__': 
    host = '0.0.0.0'
    port = 5252
    
    app.run(host = host, port = port)