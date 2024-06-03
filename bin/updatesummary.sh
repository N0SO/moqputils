#!/usr/bin/bash
#
# Run the various utilities to update database summary tables
# After new logs or changes to existing logs have been made (the 
# LOGHEADER and QSOS tables).
#
cd ~/Projects/moqputils
echo Updating SUMMARY table...
mqpcategory -c allcalls >summary-update.txt

echo Updating DIGITAL table...
mqpcategory -d allcalls >digital-update.txt

echo Updating VHF table...
mqpcategory -V allcalls >vhf-update.txt

echo Updating COUNTY table for most counties worked...
mqpcategory -m allcalls >most-counties-update.txt

echo Updating SHOWME and MISSOURI tables...
mqpcertificates -c allcalls >showme-missouri-update.txt

echo Updating ORPHANS table...
#mqporphans -c
