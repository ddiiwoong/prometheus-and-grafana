# Module04-2 Client Libraries

## Python Client Library

Python 클라이언트 라이브러리 : https://github.com/prometheus/client_python

app.py는 python flask 기반으로 작성했고 prometheus_client 라이브러리를 추가한 상태로 메트릭 HTTP endpoint(:8080)를 위한 start_http_server 를 사용한다.  
간단히 internal 500 error를 원하는 비율로 발생시키고 인위적인 메트릭으로 확인을 위해 success_rate 변수를 만들고 Gauge, Counter 로 계측을 위해서 Metric 서버(:8000)를 간단하게 구성한다.  

Counter 메트릭 타입 확인을 하기 위해 label을 http_code='500', http_code='200' 로 설정한다.  

마지막으로 Gauge 메트릭 타입으로 선언하기 위해 g.set(rate_responce) 로 설정도 추가한다.  

```python
#!/usr/bin/env python
from random import randrange
from flask import Flask
from prometheus_client import start_http_server, Gauge, Counter
import sys
app = Flask('python-library-test')
c = Counter('requests', 'Number of requests served, by http code', ['http_code'])
g = Gauge('rate_requests', 'Rate of success requests')
responce_500 = 0
responce_200 = 0
rate_responce = 0
success_rate = sys.argv[1] # internal 500 error를 원하는 비율로 발생시키기 위한 입력 인자
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
app.run(host = '0.0.0.0', port = 8080)
```

## Python Client Library

docker image로 위 sample app을 실행한다.

```
docker run -p 8888:8888 -p 8000:8000 ddiiwoong/flask-prometheus
```

## scrape 

prometheus.yml에 python client target을 추가한다. 

```
  - job_name: python_client
    static_configs:
    - targets: ['host.docker.internal:8000']
```

## Golang Client Library


