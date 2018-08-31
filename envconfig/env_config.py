#!/usr/bin/env python

import os
import sys
import argparse
import json
from util import get_platform

root_path = os.path.dirname(os.path.realpath(__file__))
default_config = os.path.join(root_path, "config.json")
platform_str = get_platform()

def read_json(json_path):
    data = {}
    if os.path.isfile(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
    return data

def get_configs(config_json):
    json_data = read_json(config_json)
    configs = {}
    configs["author"] = json_data["author"]
    configs["email"] = json_data["email"]
    platfrom_config = json_data[platform_str]
    configs.update(platfrom_config)
    return configs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="path of specified config file",
        required=False)
    args = parser.parse_args()

    config_json = args.config if args.config else default_config
    config_data = get_configs(config_json)

    pt = __import__(platform_str)
    pt.config(config_data)


if __name__ == '__main__':
    sys.exit(main())
 