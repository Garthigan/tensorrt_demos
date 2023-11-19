#!/bin/bash

echo "starting the system"
sudo systemctl enable send_count.service
sudo systemctl enable senz_obj_track.service
sudo systemctl enable device_stage_indicator.service
sudo systemctl daemon-reload
sudo systemctl start send_count.service
sudo systemctl start senz_obj_track.service
sudo systemctl start device_stage_indicator.service
sudo systemctl enable send_count.timer
sudo systemctl enable senz_obj_track.timer
sudo systemctl enable device_stage_indicator.timer
sudo systemctl daemon-reload
sudo systemctl start send_count.timer
sudo systemctl start senz_obj_track.timer
sudo systemctl start device_stage_indicator.timer
echo "system got started just now"
sleep 3

echo ""
echo "printing the status .."
echo ""

#  sudo systemctl status send_count.service
#  sudo systemctl status senz_obj_track.service
#  sudo systemctl status device_stage_indicator.service
#  sudo systemctl status send_count.timer
#  sudo systemctl status senz_obj_track.timer
#  sudo systemctl status device_stage_indicator.timer


send_count_service=$(sudo systemctl is-active send_count.service)
senz_obj_track_service=$(sudo systemctl is-active senz_obj_track.service)
device_stage_indicator_service=$(sudo systemctl is-active device_stage_indicator.service)
send_count_timer=$(sudo systemctl is-active send_count.timer)
senz_obj_track_timer=$(sudo systemctl is-active senz_obj_track.timer)
device_stage_indicator_timer=$(sudo systemctl is-active device_stage_indicator.timer)

echo "----------------------------------------------------------"
echo ""
echo "send_count_service is $send_count_service"
echo "senz_obj_track_service is $senz_obj_track_service"
echo "device_stage_indicator_service is $device_stage_indicator_service"
echo "send_count_timer is $send_count_timer"
echo "senz_obj_track_timer is $senz_obj_track_timer"
echo "device_stage_indicator_timer is $device_stage_indicator_timer"












