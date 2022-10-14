#!/bin/bash

source tools.sh

send_attack() {
    debug "Sending attack data"
    send attack -H 'Content-Type: application/json' -d '{"data":{"my_login":"TEST"},"attacker":{"source_addr":"192.168.2.4","source_port":20,"mac":"test"}}'
}

send_data() {
    debug "Sending data"
    send upload -H "Content-Disposition:inline;filename=tcpdump.pcap" -F "filename=@$FILE_NAME"
}

FILE_NAME="$@"
send_data
