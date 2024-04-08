#!/bin/bash

url=$1
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
if [ "$status_code" -eq 200 ]; then
    echo "HTTP status code 200: OK";
elif [ "$status_code" -eq 404 ]; then
    echo "HTTP status code 404: Not Found";
    exit 1;
elif [ "$status_code" -eq 500 ]; then
    echo "HTTP status code 500: Internal Server Error";
    exit 1;
else
    echo "Unexpected HTTP status code: $status_code";
    exit 1;
fi

