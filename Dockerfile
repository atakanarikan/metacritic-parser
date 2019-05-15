FROM python:3.7-slim

MAINTAINER Atakan Arikan <arikan.atakan@yahoo.com>

WORKDIR /home/docker/src

# Add requirement files
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# Add source code
COPY . .

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["main.py"]