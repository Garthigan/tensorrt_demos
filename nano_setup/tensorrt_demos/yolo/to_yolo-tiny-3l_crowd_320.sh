#!/bin/bash
set -e

echo "Creating yolov4-tiny-3l-crowdhuman-320.cfg and yolov4-tiny-3l-crowdhuman-320.weights"
cat yolov4-tiny-3l-crowdhuman-608x608.cfg | sed -e '6s/batch=32/batch=1/' | sed -e '8s/width=608/width=320/' | sed -e '9s/height=608/height=320/' > yolov4-tiny-3l-crowdhuman-320.cfg
ln -sf yolov4-tiny-3l-crowdhuman-608x608.weights yolov4-tiny-3l-crowdhuman-320.weights

echo
echo "Done."

