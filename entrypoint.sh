#!/bin/sh

celery -A tasks.app purge -f
celery -A tasks.app worker --loglevel=info 

# Wait for all background jobs to finish
wait
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        