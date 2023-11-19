#!/bin/bash
set -e

echo "Creating yolov4-crowdhuman-320.cfg and yolov4-crowdhuman-320.weights"
cat yolov4-crowdhuman-416x416.cfg | sed -e '3s/batch=24/batch=1/' | sed -e '8s/width=416/width=320/' | sed -e '9s/height=416/height=320/' > yolov4-crowdhuman-320.cfg
ln -sf yolov4-crowdhuman-416x416.weights yolov4-crowdhuman-320.weights

echo
echo "Done."

