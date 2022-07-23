FROM centos:stream8

RUN yum update -y
RUN yum install python3 -y


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 honeypot.py