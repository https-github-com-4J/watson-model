from http.server import BaseHTTPRequestHandler, HTTPServer
from watson_developer_cloud import VisualRecognitionV3 as vr
import json
import requests
import logging
import conf

port = 8083
img = "caracteres/009.png"

class S(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        with open(img, 'rb') as fp:
            response = requests.post(
                conf.watson_url,
                files=dict(upload=fp),
                headers={'Authorization': conf.watson_token})

            r = json.loads(response.text)
            to_return = json.dumps(r['results'][0])

        self.wfile.write(bytes(to_return, "utf-8"))
        logging.info(" [status:200] [license_plate:" + str(r['results'][0]['plate']) + "] [score:" + str(r['results'][0]['score']) + "]")

def run(server_class=HTTPServer, handler_class=S, port=port):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(' watson-model listening at port ' + str(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()