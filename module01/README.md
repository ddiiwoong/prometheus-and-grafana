## 1단계 - Prometheus 구성  

Prometheus 서버에는 메트릭 액세스 빈도와 함께 스크랩할 엔드포인트를 정의하는 configuration 파일이 필요하다.  

구성의 전반부는 interval을 정의하고, 후반부는 Prometheus가 데이터를 스크랩해야 하는 서버와 포트를 정의한다.  

9090은 Prometheus 자체 서비스 포트이다.  
9100은 Node Exporter 서비스 포트이다.  

[https://github.com/prometheus/prometheus/wiki/Default-port-allocations](https://github.com/prometheus/prometheus/wiki/Default-port-allocations)에서 Prometheus Eco-system이 사용하는 기폰 포트에 대해서 확인할 수 있다.  

#### prometheus.yml 
```yaml
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['127.0.0.1:9090', 'localhost:9100']
        labels:
          group: 'prometheus'
```



```
docker run -it -d -p 9090:9090 \
    -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml \
    --name prometheus-server \
    prom/prometheus
```

```
docker run -d \
  --net="host" \
  --pid="host" \
  -v "/:/host:ro,rslave" \
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```
