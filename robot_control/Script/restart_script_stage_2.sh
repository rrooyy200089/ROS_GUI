#!/bin/bash

# gnome-terminal -t "Meteor Controller" --tab -- bash -c 'roslaunch four_wheel_car_controller driver.launch'
# sleep 2

# gnome-terminal -t "ZED2 Stereo Camera" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/ZED2.launch'
# sleep 3

# gnome-terminal -t "RTAB-Map" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/CeilingSLAMwithZED2.launch localization:=true'
# sleep 1

# while true; do
#     # 使用 rostopic echo 抓取 frame_id
#     frame_id=$(rostopic echo -n 10 /tf/transforms[0]/header/frame_id 2>/dev/null | tr -d '"')

#     # echo -e "$frame_id"
    
#     # 如果抓到的資料是 "map"
#     if [[ "$frame_id" == *"map"* ]]; then
#         # echo "Frame ID is 'map'. Proceeding to the next steps..."
#         break
#     # else
#         # echo "Current Frame ID: $frame_id. Retrying..."
#         # sleep 0.1  # 等待 1 秒後重試
#     fi
# done

gnome-terminal -t "move_base" --tab -- bash -c 'roslaunch car_controller Meteor_navigation_3DLiDAR.launch'
sleep 2

gnome-terminal -t "Topology map" --tab -- bash -c 'roslaunch ~/Launch/TopologyMap.launch'
sleep 1

gnome-terminal -t "laser scan" --tab -- bash -c 'roslaunch laser_scan_obstacle_detection realsense_laser_scan_obstacle_detection.launch'
sleep 1

gnome-terminal -t "apriltag detection" --tab -- bash -c 'roslaunch apriltag_ros continuous_detection_4WDD.launch'
sleep 1

gnome-terminal -t "PBVS" --tab -- bash -c 'roslaunch forklift_server PBVS_server_4WDD.launch'
sleep 1

roslaunch robot_control gui.launch
# gnome-terminal -t "GUI" --tab -- bash -c 'roslaunch robot_control gui.launch'
# sleep 1