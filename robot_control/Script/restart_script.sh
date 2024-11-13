#!/bin/bash

gnome-terminal -t "Meteor Controller" -x bash -c 'roslaunch dashgo_driver demo.launch '
sleep 1

gnome-terminal -t "GUI" -x bash -c 'roslaunch robot_control gui.launch'
sleep 1