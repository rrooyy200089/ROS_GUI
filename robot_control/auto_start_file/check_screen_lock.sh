#!/bin/bash

export DISPLAY=$(echo $DISPLAY)
export XAUTHORITY=/home/$USER_NAME/.Xauthority

USER=$(whoami)
SESSION_ID=$(loginctl | grep $USER | awk '{print $1}')

if [[ -z "$SESSION_ID" ]]; then
    echo "無法獲取 Session ID，可能是錯誤的用戶。" >> /home/roy/screen_log.txt
    exit 1
fi

while true; do
    SESSION_STATUS=$(loginctl show-session $SESSION_ID -p LockedHint | awk -F= '{print $2}')
    
    if [[ "$SESSION_STATUS" != "no" ]]; then
        break
    fi
    echo "等待畫面鎖定... $(date)" >> /home/roy/screen_log.txt
    sleep 1  # 每秒檢查一次，避免 CPU 過度使用
done

sudo -E -u roy systemctl --user start screen_unlock.target
