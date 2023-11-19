#!/bin/bash

echo "stoping all service and timer files  ... "
sudo systemctl stop send_count.service
sudo systemctl stop senz_obj_track_1.service
sudo systemctl stop senz_obj_track_2.service
sudo systemctl stop device_stage_indicator.service
sudo systemctl stop send_count.timer
sudo systemctl stop senz_obj_track_1.timer
sudo systemctl stop senz_obj_track_2.timer
sudo systemctl stop device_stage_indicator.timer
echo "all service and timer files was stoped"
echo ""
sleep 3

send_count_service=$(sudo systemctl is-active send_count.service)
senz_obj_track_1_service=$(sudo systemctl is-active senz_obj_track_1.service)
senz_obj_track_2_service=$(sudo systemctl is-active senz_obj_track_2.service)
device_stage_indicator_service=$(sudo systemctl is-active device_stage_indicator.service)
send_count_timer=$(sudo systemctl is-active send_count.timer)
senz_obj_track_1_timer=$(sudo systemctl is-active senz_obj_track_1.timer)
senz_obj_track_2_timer=$(sudo systemctl is-active senz_obj_track_2.timer)
device_stage_indicator_timer=$(sudo systemctl is-active device_stage_indicator.timer)

echo "send_count_service is $send_count_service"
echo "senz_obj_track_1_service is $senz_obj_track_1_service"
echo "senz_obj_track_2_service is $senz_obj_track_2_service"
echo "device_stage_indicator_service is $device_stage_indicator_service"
echo "send_count_timer is $send_count_timer"
echo "senz_obj_track_1_timer is $senz_obj_track_1_timer"
echo "senz_obj_track_2_timer is $senz_obj_track_2_timer"
echo "device_stage_indicator_timer is $device_stage_indicator_timer"
