import sys
import os.path
import pdb
import glob
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess

from phytooracle_data.level1 import Level1BaseClass
from phytooracle_data import get_data

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)

# Deal with local machine paths, etc.
import dotenv
env_file = dotenv.find_dotenv(usecwd=True)
dotenv.load_dotenv(env_file)
parsed_dotenv = dotenv.dotenv_values()


class Scanner3dTop(Level1BaseClass):
    """
    import phytooracle_data.scanner3dTop
    d3 = phytooracle_data.scanner3dTop.Scanner3dTop(season=10)
    print(d3.irods_root_path)
    d3.get_dates()
    print(d3.dates)
    """
    sensor_name = "scanner3DTop"    # This doesn't exist.  Overwrite when you use this class.

    def get_dates(self):
        if len(self.file_list) == 0:
            self.get_file_list()
        wanted_files = [x.replace("  C- ", "") for x in self.file_list if len(x.split("/")[-1].split("-")) == 3]
        self.dates = [x.split("/")[-1] for x in wanted_files]
        return self.dates
