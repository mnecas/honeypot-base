#!/bin/bash

file=/tmp/afile
maxsize=100 # 100 MiB

while inotifywait -e modify "$file"; do
    actualsize=$(du -m "$file" | cut -f1)
    echo "size"
    if [ $actualsize -ge $maxsize ]; then
        echo "size is over $maxsize kilobytes"
        exit
    else
        echo "size is under $maxsize kilobytes"
    fi
done
