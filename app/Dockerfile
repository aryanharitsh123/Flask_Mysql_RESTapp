FROM python:3.8.5-alpine
COPY . /app
WORKDIR /app
RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev rust
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]