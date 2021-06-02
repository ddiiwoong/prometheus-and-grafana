#!/usr/bin/env python
from random import randrange, random
from flask import Flask
from prometheus_client import start_http_server, Gauge, Counter, Summary, Histogram
import os
import time

app = Flask('python-library-test')
c = Counter('flask_requests', 'Number of requests served, by http code', ['http_code'])
g = Gauge('flask_rate_requests', 'Rate of success requests')
s = Summary('flask_request_process_time', 'Time spent processing a request')
h = Histogram('flask_request_duration_seconds', 'Description of histogram')

responce_500 = 0
responce_200 = 0
rate_responce = 0
success_rate = os.environ['SUCCESS_RATE'] # internal 500 error를 원하는 비율로 발생시키기 위한 파라미터
@app.route('/')
@s.time()
def hello():
    global responce_500
    global responce_200
    global rate_responce
    if randrange(1, 100) > int(success_rate):
        start = time.time()
        c.labels(http_code='500').inc()
        responce_500 = responce_500 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        g.set(rate_responce)
        s.observe((time.time() - start)*1000)
        h.observe((time.time() - start)*1000)
        return "Internal Server Error\\n", 500
    else:
        start = time.time()
        c.labels(http_code='200').inc()
        responce_200 = responce_200 + 1
        rate_responce = responce_500 / (responce_500+responce_200) * 100
        g.set(rate_responce)
        s.observe((time.time() - start)*1000)
        h.observe((time.time() - start)*1000)
        return "Hello World!\\n"
start_http_server(8000)
app.run(host = '0.0.0.0', port = 8888)
