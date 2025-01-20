#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml, os

data = {'robot_reset' : None, 'robot_goal' : None}  # reset會儲存是否重新啟動，goal會儲存關閉前到達的導航點

class SaveNavigationInfo():
    def write(program_reset = False, goal_start = "P1"):
        filename = os.path.dirname(__file__) + "/Robot_Navigation_Info.yaml"
        data['robot_reset'] = program_reset
        data['robot_goal'] = goal_start
        with open(filename, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

# if __name__ == "__main__":
#     SaveNavigationInfo.write()
# print(__name__)