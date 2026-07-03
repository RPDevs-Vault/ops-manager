#!/bin/bash
set -e

sudo modprobe zram
DEVICE=$(sudo zramctl --find --size 8G --algorithm zstd)
echo "Created $DEVICE"
sudo mkfs.xfs -f $DEVICE
sudo mkdir -p /mnt/largedata/github_runners/tmp
sudo mount -t xfs $DEVICE /mnt/largedata/github_runners/tmp
sudo chown -R llmuser:llmuser /mnt/largedata/github_runners/tmp
echo "ZRAM configured on llmadmin01 at $DEVICE"
