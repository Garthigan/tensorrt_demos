#!/bin/bash
set -e

echo "Creating yolov4-320.cfg and yolov4-320.weights"
cat yolov4.cfg | sed -e '2s/batch=64/batch=1/' | sed -e '7s/width=608/width=320/' | sed -e '8s/height=608/height=320/' > yolov4-320.cfg
ln -sf yolov4.weights yolov4-320.weights

echo
echo "Done."

