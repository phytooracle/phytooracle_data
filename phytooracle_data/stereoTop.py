import sys,os
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

raw_data_dir  = parsed_dotenv["phytooracle_data"]

class Ortho(Level1BaseClass):
    """
    import phytooracle_data.rgb
    ortho = phytooracle_data.rgb.Ortho(season=10)
    print(ortho.irods_root_path)
    ortho.get_dates()
    print(ortho.dates)
    """
    sensor_name = "stereoTop"    # This doesn't exist.  Overwrite when you use this class.

    def get_dates(self):
        return self.season.dict['complete_field_dates']['rgb']
#        if len(self.file_list) == 0:
#            self.get_file_list()
#        wanted_files = [x.replace("  C- ", "") for x in self.file_list if x.endswith("reprocessed")]
#        self.dates = [x.split("/")[-1].replace("_reprocessed","") for x in wanted_files]
#        return self.dates

    def get_ortho_for_date(self, date):
        #irods_path = f"/iplant/home/shared/phytooracle/{self.season.name()}/level_1/stereoTop/{date}_reprocessed/{date}_ortho_10pct_cubic.tif"
        if self.season.season_number == 10:
            ortho_date_dir = f"{date}_reprocessed"
            ortho_filename = f"{date}_ortho_10pct_cubic.tif"
        elif self.season.season_number == 11:
            run_result = subprocess.run(["ils", os.path.join(self.irods_base_data_path())], stdout=subprocess.PIPE).stdout
            lines = run_result.decode('utf-8').splitlines()
            line = [l.split('/')[-1] for l in lines if date in l]
            ortho_date_dir = line[0]
            ortho_filename = f"{ortho_date_dir}_ortho_10pct_cubic.tif"
            
        elif self.season.season_number >= 12:
            ortho_date_dir = f"{date}"
            ortho_filename = f"{date}_ortho_10pct_cubic.tif"
            
        
        irods_path = os.path.join(self.irods_base_data_path(),ortho_date_dir, ortho_filename)
        local_path = os.path.join(self.local_base_data_path(),ortho_date_dir, ortho_filename)
        get_data(local_path, irods_path)
        return local_path
