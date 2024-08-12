from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# defining the enpoint for the url path /generate
@app.route('/generate', methods=['POST'])

def generate():
    # getting data from the request
    data = request.json

    # getting the necessary values from the json data
    modelname = data.get("modelname")
    viewerId  = data.get("viewerid")

    # generating random number for result
    rand_num = random.randint(1, 100)

    response = {
        'reason' : modelname,
        'result' : rand_num
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
