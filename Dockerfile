FROM python:3.10.6-slim-buster

COPY . sudar/

WORKDIR sudar

ENV TZ=Europe/Moscow

RUN apt-get update -y && apt-get install -y python3-pip && apt-get install -yy tzdata

RUN cp /usr/share/zoneinfo/$TZ /etc/localtime

RUN python3 -m pip install -r requirements.txt

VOLUME ["/sudar/results"]

# В данном примере парамерты захардкожены, но передаваться они должны из CI
CMD  ["sh", "-c", "python3 -m pytest --selenoid=server -n 2 tests/test_product.py \
      --alluredir=results/"]
