import requests
import json
import sys
from flask import Flask
from flask import Flask, request, render_template

BASE_URL = "https://api.ce-cotoha.com/api/dev/nlp/"
CLIENT_ID = "MuuGfYAYxNnnsKPFVhSGtAgKEhkuciGy"
CLIENT_SECRET = "riYMxy1zCkWLOFGr"

app = Flask(__name__)
def auth(client_id, client_secret):
    token_url = "https://api.ce-cotoha.com/v1/oauth/accesstokens"
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    data = {
        "grantType": "client_credentials",
        "clientId": client_id,
        "clientSecret": client_secret
    }
    r = requests.post(token_url,
                      headers=headers,
                      data=json.dumps(data))
    return r.json()["access_token"]


def parse(sentence, access_token):
    base_url = BASE_URL
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "Authorization": "Bearer {}".format(access_token)
    }
    data = {
        "sentence": sentence,
        "type": "default"
    }
    r = requests.post(base_url + "v1/parse",
                      headers=headers,
                      data=json.dumps(data))
    return r.json()


@app.route('/')
def index():
    document = request.args.get('text')
    args = sys.argv
    if len(args) >= 2:
        document = str(args[1])

    access_token = auth(CLIENT_ID, CLIENT_SECRET)
    parse_document = parse(document, access_token)
    result_list = list()
    for chunks in parse_document['result']:
        for token in chunks["tokens"]:
            if token["pos"] != "格助詞" and token["pos"] != "連用助詞" and token["pos"] != "引用助詞" and token["pos"] != "終助詞":
                result_list.append(token["kana"])

    return (' '.join(result_list))
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
