FROM quay.io/fedora/fedora:36
WORKDIR /root/
COPY . .
USER root
RUN yum install jq tcpdump inotify-tools util-linux cronie cronie-anacron -y
CMD ["./honeypot", "start"]
