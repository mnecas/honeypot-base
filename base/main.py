#! /usr/bin/env python
from scapy.all import sniff, wrpcap
import time
import os
import uuid
import requests
import logging


def test_connection(url, timeout):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def upload_file(filepath, url, timeout):
    """
    Test
    """
    # Check connection to the server
    if not test_connection(url, timeout):
        logging.warning(
            "Could not connect to server! Filepath: {}".format(filepath))
        return False
    # Open pcap file (r - read, b - binary)
    file = open(filepath, "rb")
    # Post data to the data server
    resp = requests.post(url, data=time.time(), files={"data": file})
    # Validate reply from server
    if not resp.ok:
        logging.warning("Something went wrong! Filepath: {}".format(filepath))
        return False

    file.close()
    logging.debug(
        "Upload completed successfully! Filepath: {}".format(filepath))
    return True


def get_latest_file(path):
    # Filename has format {counter}-{uuid}.pcap
    files = sorted(
        os.listdir(path),
        key=lambda x: int(x.split("-")[0]),
        reverse=True
    )
    
    if files:
        return files[0]


def main():
    count = os.environ.get("PACKET_COUNT", 500)
    filt = os.environ.get("PACKET_FILTER", "")
    url = os.environ.get("SERVER_URL", "")
    timeout = os.environ.get("SERVER_CONNECTION_TIMEOUT", 20)
    path = os.environ.get("PACKET_PATH", "/tmp")
    if not os.path.exists(path):
        print("The path '{}' does not exists!".format(path))
        exit(1)
    counter = 0
    while True:
        resutls = sniff(count=count, filter=filt)
        filename = "{}-{}.pcap".format(counter, str(uuid.uuid4()))
        filepath = os.path.join(path, filename)
        wrpcap(filepath, resutls)
        upload_file(filepath, url, timeout)
        counter += 1


if __name__ == '__main__':
    logging.getLogger(__name__)
    main()
