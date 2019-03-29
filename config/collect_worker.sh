#!/bin/bash
celery -A app worker -Q collect_queue -l INFO