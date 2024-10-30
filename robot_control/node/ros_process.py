#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

closing_order = ['gui', 'TopologyMap', 'navigation', 'SLAM', 'ZED', 'demo']  # 設定關閉順序

class Procecss():
    def close():
        result = subprocess.run(['pgrep', '-fa', 'roslaunch|rosrun|roscore'], stdout=subprocess.PIPE)
        lines = result.stdout.decode().splitlines()

        ros_process = {}
        for line in lines:
            parts = line.split()
            pid = parts[0]
            name = ''.join(parts[3:])
            ros_process[name] = pid
            # print(f'name : {name}  PID : {pid}')

        for i in closing_order:
            for command, command_pid in ros_process.items():
                if i in command:
                    print(f'name : {command}  PID : {command_pid}')
                    # subprocess.run(['kill', '-15', command_pid])
                    # time.sleep(1)
                    break

if __name__ == '__main__':
    Procecss.close()