import sys
#import os.path
#import pdb
#import glob
#import urllib.request
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#from datetime import datetime
import subprocess

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)

from phytooracle_data.seasons import Season

import dotenv
env_file = dotenv.find_dotenv(usecwd=True)
dotenv.load_dotenv(env_file)
parsed_dotenv = dotenv.dotenv_values()

raw_data_dir  = parsed_dotenv["phytooracle_data"]

class Level1BaseClass(object):

    sensor_name = "foo"    # This doesn't exist.  Overwrite when you use this class.
    file_list = []
    dates     = []

    def __init__(self, season=None, force_download=False):
        if season is not None:
            self.season = Season(season=season)
        else:
            log.critical(f"You must provide {self.__class__} with a season or start and end dates")
            sys.exit(0)

        self.initialize_paths()

        #self.irods_root_path = f"/iplant/home/shared/phytooracle/{self.season.name()}/level_1/{self.phytooracle_dir_name}"

    def initialize_paths(self):
        pass
        return

    def base_data_path(self):
        """
        return example: 'season_10_lettuce_yr_2020/level_1/stereoTop/'
        """
        return f"{self.season.name()}/level_1/{self.sensor_name}/sorghum"

    def irods_base_data_path(self):
        """
        return example: '/iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_1/stereoTop/'
        """
        return f"/iplant/home/shared/phytooracle/" + self.base_data_path() + "sorghum/"

    def local_base_data_path(self):
        """
        return example:
        '/media/equant/big_drive/work/raw_data/season_10_lettuce_yr_2020/level_1/stereoTop/'
        """

        return raw_data_dir + "/" + self.base_data_path()

    def get_file_list(self):
        print(f"getting directory list from: {self.irods_base_data_path()}")
        run_result = subprocess.run(["ils", self.irods_base_data_path()], stdout=subprocess.PIPE).stdout
        lines = run_result.decode('utf-8').splitlines()
        self.file_list = lines

