# Module01 - Prometheus 구성  

Prometheus 서버에는 메트릭 액세스 빈도와 함께 스크랩할 엔드포인트를 정의하는 configuration 파일이 필요하다.  

구성의 전반부는 interval을 정의하고, 후반부는 Prometheus가 데이터를 스크랩해야 하는 서버와 포트를 정의한다.  

9090은 Prometheus 자체 서비스 포트이다.  
9100은 Node Exporter 서비스 포트이다.  

[https://github.com/prometheus/prometheus/wiki/Default-port-allocations](https://github.com/prometheus/prometheus/wiki/Default-port-allocations)에서 Prometheus Eco-system이 사용하는 기폰 포트에 대해서 확인할 수 있다.  


## Linux 환경

### prometheus.yml 
```yaml
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['127.0.0.1:9090']
        labels:
          group: 'prometheus'
  - job_name: node
    static_configs:
    - targets: ['exporter:9100']
```

### docker-compose로 실행
```sh
docker-compose up -d
```

### docker로 실행
```sh
docker run -it -d -p 9090:9090 \
    -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml \
    --name prometheus-server \
    prom/prometheus
```


## MacOS 환경
macOS 용 Docker에서는 네트워크를 포함한 여러가지 제약사항이 존재하므로 node_exporter를 binary형태로 실행한다.

[https://github.com/prometheus/node_exporter/issues/610](https://github.com/prometheus/node_exporter/issues/610)

```sh
curl  -OL https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.darwin-amd64.tar.gz
tar -xzf node_exporter-1.1.2.darwin-amd64.tar.gz
cd node_exporter-1.1.2.darwin-amd64
./node_exporter
```

### prometheus.yml 
```
global:
  scrape_interval:     15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['127.0.0.1:9090']
        labels:
          group: 'prometheus'
  - job_name: node
    static_configs:
    - targets: ['host.docker.internal:9100']
```

### Prometheus 실행
```
cd macos
docker run -it -d -p 9090:9090 \
    -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml \
    --name prometheus-server \
    prom/prometheus
```
