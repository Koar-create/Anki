#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json

def load_config(configFile='config.json'):
    currentDir = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(currentDir, configFile)
    if not os.path.exists(configPath):
        print(f"ERROR: {configPath} not exist, exit.")
        sys.exit()
    with open(configPath, 'r') as config_file:
        return json.load(config_file)
