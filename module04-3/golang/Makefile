VERSION=latest
PREFIX=ddiiwoong/gomux-prometheus
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
	docker run --rm -p 9001:9001 $(PREFIX):$(TAG)