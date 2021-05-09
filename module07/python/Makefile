VERSION=latest
PREFIX=ddiiwoong/flask-prometheus
TAG=$(VERSION)

all: build push

build:
	@echo "Building image:"
	docker build -t $(PREFIX):$(TAG) .
push:
	@echo "Pushing image:"
	docker push $(PREFIX):$(TAG)
test:
	@echo "Running container:"
	docker run --rm -p 8888:8888 -p 8000:8000 $(PREFIX):$(TAG)