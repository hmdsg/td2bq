from os import abort
from flask import Flask, request, abort
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True
)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/js/v3/event/foodb/test_page_views",methods=['OPTION', 'POST'])
def option():
    try:
        # For pre-flight 
        if request.method == 'OPTION':
            return
        elif request.method == 'POST':
            data = request.get_data()
            print (data.decode('utf-8'))
            return ""    
        else:
            return abort(400)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(port=8080, debug=True)