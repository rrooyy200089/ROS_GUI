#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml, os

data = {'reset' : None, 'goal' : None}

class SaveNavigationInfo():
    def write(program_reset = False, goal_start = "P1"):
        filename = os.path.dirname(__file__) + "/test.yaml"
        data['reset'] = program_reset
        data['goal'] = goal_start
        with open(filename, 'w') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False)

# if __name__ == "__main__":
#     SaveNavigationInfo.write()
# print(__name__)