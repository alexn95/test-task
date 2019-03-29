#!/bin/bash
celery -A app worker -Q processing_queue,main_queue -l INFO