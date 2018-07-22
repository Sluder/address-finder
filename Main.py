#!/usr/bin/python

import sys
import os

import Global
from EcuFile import EcuFile
from Instruction import Instruction

def _load_config(file_name):
    """
    Loads sensor labels & memory addresses (Ex: battery_voltage 0x102f)
    :param file_name: file name for config file
    """
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            for file_line in file:
                file_line = Global.format_line(file_line)

                # Format sensor addresses
                if not file_line[1].startswith("0x"):
                    file_line[1] = "0x" + file_line[1]

                Global.config[file_line[0]] = file_line[1]
        print("[success] Loaded config")
    else:
        print("[ error ] " + file_name + " doesn't exist")
        sys.exit()

def _calculate_jaccard_index(control_feature, experimental_feature):
    """
    Calculates Jaccard Index for two different feature blocks
    :param control_feature: feature for control file
    :param experimental_feature: feature for experimental file
    :return: float of Jaccard index
    """
    control_set = control_feature.get_instruction_set()
    experimental_set = experimental_feature.get_instruction_set()

    intersection = len(list(set(control_set).intersection(experimental_set)))
    union = len(control_set) + len(experimental_set) - intersection

    return float(intersection / union)

if __name__ == "__main__":
    """
    Start of program
    :param argv: array execution arguments (config.txt control.txt ecu.txt)
    """
    _load_config(sys.argv[1])

    control_file = EcuFile(sys.argv[2], True)
    experimental_file = EcuFile(sys.argv[3], False)

    print(control_file)

    # # Loop through experimental file features
    # for address, feature_set in experimental_file.features.items():
    #     for feature in feature_set.features:
    #         # Loop though control file features
    #         for control_sensor, control_feature_set in control_file.features.items():
    #             jaccard_indexes = []
    #
    #             for control_feature in control_feature_set:
    #                 value = _calculate_jaccard_index(control_feature, feature)
    #                 feature.set_jaccard_index(value)
    #                 jaccard_indexes.append(value)
