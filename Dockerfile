FROM ubuntu:latest
WORKDIR /root/
COPY . .
USER root
RUN apt-get update && apt-get install tcpdump inotify-tools util-linux -y
CMD ["./honeypot", "start"]
