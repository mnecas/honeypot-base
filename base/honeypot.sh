#!/bin/bash

# Variables
TCPDUMP_FILE=${TCPDUMP_FILE:-"/tmp/tcpdump.pcap"}
TCPDUMP_FILTER=${TCPDUMP_FILTER:-'tcp'}
# Maximum size of file in MiB
TCPDUMP_MAX_SIZE=${TCPDUMP_MAX_SIZE:-2}
# TCPDUMP_CRONTAB=${TCPDUMP_CRONTAB:-"0 * * * *"}
TCPDUMP_CRONTAB_FILE=${TCPDUMP_CRONTAB_FILE:-"/tmp/honeypot.cron"}

HONEYPOT_NAME=${HONEYPOT_NAME:-$(uuidgen)}
HONEYPOT_TYPE=${HONEYPOT_TYPE:-"general"}
HONEYPOT_ID=""
HONEYPOT_SERVER=${SERVER:-"127.0.0.1:8000"}
# LOG_PATH=/var/log/honeypot
LOG_PATH=./log/

start_tcpdump(){
    echo "Starting tcpdump"
    if [ -f $TCPDUMP_FILE ]; then
        echo "The file '$TCPDUMP_FILE' exits, removing."
        rm $TCPDUMP_FILE
    fi
    tcpdump -w $TCPDUMP_FILE $TCPDUMP_FILTER
}

start_inotify(){
    echo "Starting inotify"
    # -qq = for quite without modify
    while inotifywait -e modify "$TCPDUMP_FILE"; do
        actualsize=$(du -m "$TCPDUMP_FILE" | cut -f1)
        echo "$actualsize"
        if [ $actualsize -ge $TCPDUMP_MAX_SIZE ]; then
            echo "Size is over $TCPDUMP_MAX_SIZE megabytes"
            send_data
        fi
    done
}

# start_crontab(){
#     echo "Starting crontab setup"
#     echo "$TCPDUMP_CRONTAB /usr/bin/honeypot.sh send_data" > $TCPDUMP_CRONTAB_FILE
#     chmod +x $TCPDUMP_CRONTAB_FILE
#     crontab $TCPDUMP_CRONTAB_FILE
#     echo "Finished crontab setup"
# }

send_attack() {
    echo "Sending data"
    curl \
        -H "Authorization: Token $TOKEN" \
        -H 'Content-Type: application/json' \
        -d '{"data":{"my_login":"TEST"},"attacker":{"source_addr":"192.168.2.4","source_port":20,"mac":"test"}}' \
        --connect-timeout 5 \
        --max-time 10 \
        --retry 5 \
        --retry-delay 0 \
        --retry-max-time 40 \
        http://$HONEYPOT_SERVER/api/honeypots/$ID/attack
}

send_data() {
    echo "Sending data"
    curl \
        -H "Content-Disposition:inline;filename=tcpdump.pcap" \
        -H "Authorization: Token $TOKEN" \
        -F "filename=@$TCPDUMP_FILE" \
        --connect-timeout 5 \
        --max-time 10 \
        --retry 5 \
        --retry-delay 0 \
        --retry-max-time 40 \
        http://$HONEYPOT_SERVER/api/honeypots/$ID/upload
    kill $(cat tcpdump-pid)
}

init(){
    # Setup log path
    if [ -d $LOG_PATH ]; then
        echo "Cleanup of logs"
        rm -f $LOG_PATH/*
    else
        mkdir -p $LOG_PATH
    fi

    echo "Init of the honeypot"
    init_data=$(curl -d "type=$HONEYPOT_TYPE&name=$HONEYPOT_NAME" -X POST http://$HONEYPOT_SERVER/api/honeypots/)
    TOKEN=$(echo $init_data | jq -j '.token')
    ID=$(echo $init_data | jq -j '.id')
}

start_tcpdump_process(){
    start_tcpdump &>> $LOG_PATH/tcpdump.log &
    TCPDUMP_PID="$!"
    echo "$TCPDUMP_PID" > tcpdump-pid
    echo "Started tcpdump process with PID $TCPDUMP_PID"
}

start(){
    init

    # Start of tcpdump
    start_tcpdump_process

    # Wait for TCPDUMP_FILE to be created
    sleep .1

    # Start inotify
    start_inotify &>> $LOG_PATH/inotify.log &
    inotify_pid="$!"
    echo "Started inotify process with PID $inotify_pid"

    # Start crontab
    # echo "Started crontab"
    # start_crontab

    while true; do
        wait $TCPDUMP_PID
        start_tcpdump_process
    done
}

$1
