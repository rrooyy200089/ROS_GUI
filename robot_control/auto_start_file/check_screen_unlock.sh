#!/bin/bash

export DISPLAY=$(echo $DISPLAY)
export XAUTHORITY=/home/$USER_NAME/.Xauthority

USER=$(whoami)
SESSION_ID=$(loginctl | grep $USER | awk '{print $1}')
PROJECT_PATH=$(find ~/ -name restart_script_stage_1.sh) #取得專案路徑

if [[ -z "$SESSION_ID" ]]; then
    echo "無法獲取 Session ID，可能是錯誤的用戶。" >> /home/$USER/screen_log.txt
    exit 1
fi

while true; do
    SESSION_STATUS=$(loginctl show-session $SESSION_ID -p LockedHint | awk -F= '{print $2}')
    
    if [[ "$SESSION_STATUS" == "no" ]]; then
        break
    fi
    sleep 1  # 每秒檢查一次，避免 CPU 過度使用
done

# 當畫面解鎖時，紀錄當前時間
UNLOCK_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "畫面已解鎖，時間：$UNLOCK_TIME" >> /home/$USER/screen_log.txt

source ~/.bashrc
# roslaunch robot_control gui.launch
gnome-terminal -- bash -c "$PROJECT_PATH"
