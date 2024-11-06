#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

class Procecss():
    # def close():
    #     result = subprocess.run(['pgrep', '-fa', 'roslaunch|rosrun|roscore'], stdout=subprocess.PIPE)
    #     lines = result.stdout.decode().splitlines()

    #     ros_process = {}
    #     for line in lines:
    #         parts = line.split()
    #         pid = parts[0]
    #         name = ''.join(parts[3:])
    #         ros_process[name] = pid
    #         # print(f'name : {name}  PID : {pid}')

    #     for i in closing_order:
    #         for command, command_pid in ros_process.items():
    #             if i in command:
    #                 if 'gui' in command: window.close()
    #                 print(f'name : {command}  PID : {command_pid}')
    #                 subprocess.run(['kill', '-15', command_pid])
    #                 time.sleep(1)
    #                 break

    def restart():
        try:
            # 使用 subprocess.run 執行指令
            result = subprocess.run('/home/ericlai/project/gui_ws/src/robot_control/node/test.sh', shell=True, capture_output=True, text=True)
            
            # 判斷是否執行成功
            if result.returncode == 0:
                print("Command executed successfully.")
                print("Output:")
                print(result.stdout)  # 輸出結果
            else:
                print("Command failed with return code:", result.returncode)
                print("Error message:")
                print(result.stderr)  # 錯誤訊息
        except Exception as e:
            print("An error occurred while running the command:", e)

if __name__ == '__main__':
    Procecss.restart()
    print('restart!')