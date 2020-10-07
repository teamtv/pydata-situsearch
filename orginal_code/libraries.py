# Data manipulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Display options for pandas
pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# Display options for numpy
np.set_printoptions(linewidth=120, suppress=True)

# Display options for pyplot
%config InlineBackend.figure_format = 'retina'

## Cell computation timer
%load_ext autotime

import glob
import random

import sys
np.set_printoptions(threshold=sys.maxsize)

import scipy.stats as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

from tqdm import tqdm_notebook as tqdm
