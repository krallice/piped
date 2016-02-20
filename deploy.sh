#!/bin/bash

echo "Deploying Locally ..."

# Directory setup:
mkdir -v /var/lib/piped
touch /var/lib/piped/piped.cache
chown -Rv root.root /var/lib/piped

# Copy Files:
cp -pv piped /usr/local/bin/
chown -v root.root /usr/local/bin/piped

cp -pv *yaml /usr/local/etc/
chown -v root.root /usr/local/etc/piped*yaml

# Copy systemd unit file:
cp -pv piped.service /etc/systemd/system/
chown -v root.root /etc/systemd/system/piped.service
