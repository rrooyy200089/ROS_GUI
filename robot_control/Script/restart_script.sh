#!/bin/bash

gnome-terminal -t "Meteor Controller" --tab -- bash -c 'roslaunch four_wheel_car_controller driver.launch'
sleep 1

gnome-terminal -t "ZED2 Stereo Camera" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/ZED2.launch'
sleep 1

gnome-terminal -t "RTAB-Map" --tab -- bash -c 'roslaunch ~/Launch/ZED2_VisualSLAM/CeilingSLAMwithZED2.launch localization:=true'
sleep 1

gnome-terminal -t "move_base" --tab -- bash -c 'roslaunch car_controller Meteor_navigation_3DLiDAR.launch'
sleep 1

gnome-terminal -t "Topology map" --tab -- bash -c 'roslaunch ~/Launch/TopologyMap.launch'
sleep 1

gnome-terminal -t "laser scan" --tab -- bash -c 'roslaunch laser_scan_obstacle_detection realsense_laser_scan_obstacle_detection.launch'
sleep 1

gnome-terminal -t "GUI" --tab -- bash -c 'roslaunch robot_control gui.launch'
sleep 1