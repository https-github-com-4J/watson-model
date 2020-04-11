from flask import Flask, request, Response
from random import randint
from watson_developer_cloud import VisualRecognitionV3 as vr
import jsonpickle
import numpy as np
import cv2
import json
import requests
import conf

app = Flask(__name__)
random_min = 1000000000
random_max = 9999999999

@app.route('/execute/watson', methods=['POST'])
def test():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img_name = 'platesimg/' + str(randint(random_min, random_max)) + '.jpg'
    cv2.imwrite(img_name, img);

    with open(img_name, 'rb') as fp:
        response = requests.post(
            conf.watson_url,
            files=dict(upload=fp),
            headers={'Authorization': conf.watson_token})

    r = json.loads(response.text)
    to_return = json.dumps(r['results'][0])
    response_pickled = jsonpickle.encode(r['results'][0])

    return Response(response=response_pickled, status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=8088)