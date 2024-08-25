#!/bin/sh

# Start the Celery worker
celery -A tasks.app worker --loglevel=info &

sleep 15
# Run the Python consumer script
echo "Listing files:" && ls -la

python run_consumer.py

# Wait for all background jobs to finish
wait
