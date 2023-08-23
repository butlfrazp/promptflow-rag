#!/bin/env bash

# Sleep until the .env_ready file is created
notified=0
while [ ! -f ~/.env_ready ]; do
    if [ $notified -eq 0 ]; then
        echo "Waiting for environment to finish initializing..."
        notified=1
    fi
    sleep 1
done

# Notify user that environment is ready
if [ $notified -eq 1 ]; then
    echo "Environment ready!"
fi
