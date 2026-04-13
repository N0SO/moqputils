#! /bin/env bash
# Fetch the latest MOQP logs from W0MA
# Brute force, needs generalization.
#
YEAR=2026
DESTINATION=/home/pi/Public/moqplogs/$YEAR
SOURCE=w0ma@w0ma.org:/home/w0ma/mo_qso_party/results/$YEAR/logs
cd $DESTINATION

# Redirect all output to log file
exec >> file-downloadlog.txt 2>&1
echo "---------> start of download: "; date
rsync --stats -av  $SOURCE/ logfiles/from_w0ma

