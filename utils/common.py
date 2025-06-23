#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import glob          # usage: deep search
import json
import numpy as np
import pandas as pd
import platform      # usage: verify the OS
import re            # usage: process regularized expression
import shutil        # usage: process files
import time          # usage: stat elapsed time
import warnings

from   load_config     import load_config
from   print_record    import print_record
from   send_email      import *

# ingore warnings

# extra font loading

# extract color constant
config   = load_config()
colors   = config['colors']
gold     = colors['gold']
red      = colors['red']
green    = colors['green']
yellow   = colors['yellow']
blue     = colors['blue']
purple   = colors['purple']
aquablue = colors['aquablue']
gray     = colors['gray']
reset    = colors['reset']
