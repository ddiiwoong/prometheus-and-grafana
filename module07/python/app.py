#!/usr/bin/env python
from random import randrange
from flask import Flask
from prometheus_client import start_http_server, Gauge, Counter
import os
app = Flask('python-library-test')
c = Counter('flask_requests', 'Number of requests served, by http code', ['http_code'])
g = Gauge('flask_rate_requests', 'Rate of success requests')
responce_500 = 0
responce_200 = 0
rate_responce = 0
success_rate = os.environ['SUCCESS_RATE'] # internal 500 error를 원하는 비율로 발생시키기 위한 파라미터
@app.route('/')
def hello():
    global responce_500
    global responce_200
    global rate_responce
    if randrange(1, 100) > int(success_rate):
        c.labels(http_code='500').inc()
        responce_500 = responce_500 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        g.set(rate_responce)
        return "Internal Server Error\\n", 500
    else:
        c.labels(http_code='200').inc()
        responce_200 = responce_200 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        g.set(rate_responce)
        return "Hello World!\\n"
start_http_server(8000)
app.run(host = '0.0.0.0', port = 8888)