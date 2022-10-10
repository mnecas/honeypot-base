FROM quay.io/fedora/fedora:36
WORKDIR /honeypot
COPY . /honeypot/
USER root
RUN yum install jq tcpdump inotify-tools util-linux -y
CMD ["/honeypot/base/honeypot.sh", "start"]
