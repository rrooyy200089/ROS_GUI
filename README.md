# ROS_GUI

## Description

Ubuntu 20.04 ROS noetic

PyQt5 Version: 5.14.1

## Installation

### Install Project
```
$ mkdir ~/gui_ws
$ cd ~/gui_ws
$ git clone https://github.com/rrooyy200089/ROS_GUI.git src
$ catkin_make
$ echo "source ~/gui_ws/devel/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
$ chmod +x ~/gui_ws/src/robot_control/Script/restart_script.sh
```

### Install Package
```
$ sudo apt-get install python3-pyqt5.qtmultimedia
$ sudo apt-get install libqt5multimedia5-plugins
```

### Install Fonts
```
sudo cp ~/gui_ws/src/robot_control/fonts/kaiu.ttf /usr/share/fonts/truetype/
sudo mkfontdir /usr/share/fonts/truetype/
sudo fc-cache -fv
```
