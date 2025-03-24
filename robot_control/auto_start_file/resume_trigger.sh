#!/bin/bash
if [ "$1" = "post" ]; then
    echo "Resume detected, triggering user target at $(date)" >> /home/roy/resume_log.txt
    user_id=$(id -u roy)
    export XDG_RUNTIME_DIR="/run/user/$user_id"
    sudo -E -u roy systemctl --user start after-resume.target >> /home/roy/resume_log.txt 2>&1
fi

