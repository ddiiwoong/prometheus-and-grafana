FROM python:3.9-slim

ENV SUCCESS_RATE=80
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
STOPSIGNAL SIGINT
ENTRYPOINT ["python"]
CMD ["app.py"]