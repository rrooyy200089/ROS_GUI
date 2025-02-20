#!/bin/bash

gnome-terminal -t "Meteor Controller" --tab -- bash -c 'roslaunch four_wheel_car_controller driver.launch'
sleep 2

gnome-terminal -t "ZED2 Stereo Camera" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/ZED2.launch'
sleep 2

gnome-terminal -t "D435 Camera" --tab -- bash -c 'roslaunch apriltag_ros D435Camera_4WDD.launch'
sleep 2

gnome-terminal -t "RTAB-Map" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/CeilingSLAMwithZED2.launch localization:=true'
sleep 1

while true; do
    # 使用 rostopic echo 抓取 frame_id
    frame_id=$(rostopic echo -n 10 /tf/transforms[0]/header/frame_id 2>/dev/null | tr -d '"')

    # echo -e "$frame_id"
    
    # 如果抓到的資料是 "map"
    if [[ "$frame_id" == *"map"* ]]; then
        # echo "Frame ID is 'map'. Proceeding to the next steps..."
        break
    # else
        # echo "Current Frame ID: $frame_id. Retrying..."
        # sleep 0.1  # 等待 1 秒後重試
    fi
done

~/project/gui_ws/src/robot_control/Script/restart_script_stage_2.sh

# gnome-terminal -t "move_base" --tab -- bash -c 'roslaunch car_controller Meteor_navigation_3DLiDAR.launch'
# sleep 1

# gnome-terminal -t "Topology map" --tab -- bash -c 'roslaunch ~/Launch/TopologyMap.launch'
# sleep 1

# gnome-terminal -t "laser scan" --tab -- bash -c 'roslaunch laser_scan_obstacle_detection realsense_laser_scan_obstacle_detection.launch'
# sleep 1

# python3 ~/project/gui_ws/src/robot_control/Script/test.py
# ~/project/gui_ws/src/robot_control/Script/restart_script2.sh
# roslaunch robot_control gui.launch
# gnome-terminal -t "GUI_PY" --tab -- bash -c '~/project/gui_ws/src/robot_control/Script/test.py'
# sleep 1