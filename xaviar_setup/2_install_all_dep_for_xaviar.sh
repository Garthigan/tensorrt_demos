#!/bin/bash

echo "installing tensorflow ..."
sudo apt update 
sudo apt install nvidia-jetpack -y
echo -e "nvidia-jetpack was installed sucsussfully"

echo "setting the cuda path ..."
line1='export PATH=${PATH}:/usr/local/cuda/bin'
line2='export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64'
line3='export PATH=$PATH:~/.local/bin'


if ! grep -qF "$line1" ~/.bashrc; then
    echo "$line1" >> ~/.bashrc
fi
if ! grep -qF "$line2" ~/.bashrc; then
    echo "$line2" >> ~/.bashrc
fi
if ! grep -qF "$line3" ~/.bashrc; then
    echo "$line3" >> ~/.bashrc
fi
# Save and close the .bashrc file
source ~/.bashrc
echo -e "cuda path was set"


echo "installing tensorflow ..."
sudo apt-get update 
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran 
sudo apt-get install python3-pip 
sudo python3 -m pip install --upgrade pip 
sudo pip3 install -U testresources setuptools==65.5.0 
sudo pip3 install -U numpy==1.22 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig packaging h5py==3.6.0 
sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v511 tensorflow==2.12.0+nv23.4 
echo -e "tensorflow was installed sucsussfully"

echo "installing othe rdependencies ..."
pip3 install opencv-python 
pip3 install --no-cache-dir --global-option=build_ext --global-option="-I/usr/local/cuda-11.4/targets/aarch64-linux/include/" --global-option="-L/usr/local/cuda-11.4/targets/aarch64-linux/lib/" pycuda==2020.1 
sudo pip3 install onnx 
pip install easydict 
pip install paho-mqtt 
pip install psutil 
echo -e  "package installing is dene ..."














