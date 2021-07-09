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

    def download_untar_heatmap_for_date(self,use_date):
        
        # tar -xvf 2020-01-18_heat_map.tar

        # Figure out if we need to download the data.
        need_to_download_data = False
        heatmap_file_name = os.path.join(self.irods_base_data_path(),use_date,"{0}_heat_map.tar".format(use_date))
        season_dir_name = self.season.name()
        three_dee_raw_path = os.path.join(parsed_dotenv["phytooracle_data"], season_dir_name)
        three_dee_raw_tar_file = os.path.join(three_dee_raw_path, "{0}_heat_map.tar".format(use_date))
        three_dee_folder_path = os.path.join(three_dee_raw_path, "heatmap_out")

        if not os.path.isdir(three_dee_folder_path):
            # Data doesn't exist locally
            log.info(f"Didn't find {three_dee_folder_path}, fetching it with irods...")
            need_to_download_data = True
        
        if self.force_download:
            if not need_to_download_data:
                # Data exists locally, but we're going to overwrite it.
                log.info(f"Found local rgb data, but we've been asked to re-download it with the force_download flag")
                need_to_download_data = True

        if need_to_download_data:
            os.makedirs(three_dee_raw_path, exist_ok=True)
            import shutil
            if shutil.which('iget') is None:
                log.critical(f"You need to install irods so we can fetch the data")
                sys.exit(0)
            import subprocess
            
            result = subprocess.run(["iget", "-N", "0", "-rKPVT", heatmap_file_name])
            if result.returncode != 0:
                log.critical(f"iget did not complete successfully... {result}")
                sys.exit(0)
            
            # Untarring the individual plants tar file
            
            result = subprocess.run(["tar", "-xvf", three_dee_raw_tar_file, "-C", three_dee_folder_path])
            if result.returncode != 0:
                log.critical(f"untaring did not complete successfully... {result}")
                sys.exit(0)

            result = subprocess.run(["rm", three_dee_raw_tar_file])
            if result.returncode != 0:
                log.critical(f"could not successfully delete the tar file... {result}")
                sys.exit(0)
                