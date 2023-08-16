
# Respiration recording analysis toolbox

This library provides python functions to evaluate single belt chest expansion recordings of human adult respiration during passive tasks (standing still, sitting and listening to music, etc.) It includes functions to find and describe features of individual breaths and to evaluate important phases of the respiratory cycle.

Fuction for respiration analysis packaged within the module respy.py.

Packaged with it, for phase alignment assessment, is the activity analysis toolbook, within the module act.py

Developed by Finn Upham 2023 

This is not yet suitable for the evaluation of respiration during high intensity exertions, or for non-human animals, or for respiration measurements taken with other types of sensors (flow meters, double belts).

This toolbox is written in python 3.9 with the following dependencies:
import time
import datetime as dt
import math
import numpy as np 
import pandas as pd
import scipy as sc 
from scipy.signal import butter,filtfilt
from scipy import interpolate
from scipy.interpolate import interp1d


## Installation
Add the package with pip with the code above like: 
> pip install respy

## Example respiration analysis

Find demo application this github account Finn42
https://github.com/finn42/respydemo

Activity analysis demo (with test package or loaded definitions)
https://github.com/finn42/aa_test_package

