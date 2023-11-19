

if [ -e /home/nvidia/Downloads/tensorrt_demos/plugins/libyolo_layer.so ]; then
    rm /home/nvidia/Downloads/tensorrt_demos/plugins/libyolo_layer.so
fi


cd /home/nvidia/Downloads/tensorrt_demos/plugins
make

cd /home/nvidia/Downloads/tensorrt_demos/yolo
echo -e "converting yolov4-tiny-3l-ch-2203-416.weight model to onnx ..."
python3 yolo_to_onnx.py -m yolov4-tiny-3l-ch-2203-416
echo -e "converting yolov4-tiny-3l-ch-2203-41.onnx model to trt ..."
python3 onnx_to_tensorrt.py -m yolov4-tiny-3l-ch-2203-416

echo -e "succsusfully built TRT model"



