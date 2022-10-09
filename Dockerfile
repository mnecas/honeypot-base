FROM quay.io/centos/centos:stream8
WORKDIR /honeypot
COPY . /honeypot/
RUN yum install jq -y
CMD ["/honeypot/base/honeypot.sh", "start"]
