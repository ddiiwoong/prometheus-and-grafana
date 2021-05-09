# Client Libraries

## Python Client Library


```
docker run -p 8888:8888 -p 8000:8000 ddiiwoong/flask-prometheus
```

## scrape 

```
  - job_name: python_client
    static_configs:
    - targets: ['host.docker.internal:8000']
```
