from os import abort
from flask import Flask, request, abort
from flask_cors import CORS
from google.cloud import pubsub_v1
import json
import datetime

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True
)

# PubSub Settings
project_id = "td2bq-360607"
topic_id = "td-topic"
publisher = pubsub_v1.PublisherClient()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/js/v3/event/<db>/<table>",methods=['OPTIONS', 'POST'])
def test_view(db,table):
    print (f"db:{db}")
    print (f"table:{table}")

    try:
        # For pre-flight 
        if request.method == 'OPTIONS':
            return ""
        elif request.method == 'POST':
            data = request.get_data()
            print (data.decode('utf-8'))

            # Convert for editing
            dict = json.loads(data.decode('utf-8'))
            send_pubsub(dict)
            
            return ""    
        else:
            return abort(400)
    except Exception as e:
        return str(e)

def send_pubsub(data_dict:dict):

    # Add server timestamp
    dt = datetime.datetime.now()
    ut = dt.timestamp() * 1000000
    data_dict["timestamp"] = int(ut)
    
    print(int(ut))
    data_str = json.dumps(data_dict)
    print (data_str)
    
    data = data_str.encode("utf-8")
    topic_path = publisher.topic_path(project_id, topic_id)
    print(data)
    future = publisher.publish(topic_path, data)
    print (future.result()) 


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)