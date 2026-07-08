#!/bin/bash
set -e

sudo modprobe zram
DEVICE=$(sudo zramctl --find --size 2G --algorithm zstd)
echo "Created $DEVICE"
sudo mkfs.xfs -f $DEVICE
sudo mkdir -p /mnt/data/github_runners/tmp
sudo mount -t xfs $DEVICE /mnt/data/github_runners/tmp
sudo chown -R user:user /mnt/data/github_runners/tmp
echo "ZRAM configured on T430 at $DEVICE"
