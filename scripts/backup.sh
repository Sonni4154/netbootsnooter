#!/bin/sh
set -eu
ts=$(date +%F)
mkdir -p backup
tar czf backup/backup-$ts.tar.gz vars.txt client.txt logs || true
echo "Backup created at backup/backup-$ts.tar.gz"
