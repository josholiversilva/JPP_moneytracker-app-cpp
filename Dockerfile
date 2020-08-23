#Docker file for MoneyTracker APP

FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

COPY . /mnt
WORKDIR /mnt

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["moneytracker.py"]

