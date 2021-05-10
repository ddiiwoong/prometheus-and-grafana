# Pushgateway

## Pushgateway 설치
```sh
docker run -d -p 9091:9091 prom/pushgateway
```
### metrics 확인
[http://localhost:9091/metrics](http://localhost:9091/metrics)

## prometheus scrape config

prometheus.yml에 nginx target을 추가한다.  
`honor_labels: true`는 Pushgateway가 expose하는 모든 레이블을 보존하려는 경우에 사용한다.

```
  - job_name: pushgateway
    honor_labels: true
    static_configs:
    - targets: ['host.docker.internal:9091']
```

다시 prometheus 서버를 실행한다.
```
docker run -it -d -p 9090:9090 \
    -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml \
    --name prometheus-server \
    prom/prometheus
```

## pushgateway metric 확인

`pushgateway_build_info`로 pushgateway 빌드 정보를 알수 있다. 

## push custom metric

-data-binary @- flag로 메트릭 정보를 인자로 넘깁니다.

```
echo "pi_metric 3.14" | curl --data-binary @- http://localhost:9091/metrics/job/some_job
```


{job="some_job",instance="some_instance"} label을 가지는 counter와 gauge를 push 한다. 

```
cat <<EOF | curl --data-binary @- http://localhost:9091/metrics/job/some_job/instance/some_instance
# TYPE steps counter
# HELP steps is number of walk steps
steps{label="applewatch"} 4340
# TYPE pulse gauge
# HELP pulse is heart rate
pulse 89
EOF
```

Push metric을 확인할수 있다.

```
curl http://localhost:9091/metrics
... 
pulse{instance="some_instance",job="some_job"} 89
...
steps{instance="some_instance",job="some_job",label="applewatch"} 4340
```
