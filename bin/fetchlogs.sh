#! /bin/env bash
# Fetch the latest MOQP logs from W0MA
# Brute force, needs generalization.
#
cd /home/pi/Public/moqplogs/2025
# Redirect all output to log file
exec >> file-downloadlog.txt 2>&1
echo "---------> start of download: "; date
rsync --stats -av  w0ma@w0ma.org:/home/w0ma/mo_qso_party/results/2025/logs/ ./logfiles/from_w0ma

