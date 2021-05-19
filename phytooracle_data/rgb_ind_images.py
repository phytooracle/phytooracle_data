import sys
import os.path
import os
import glob
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


from phytooracle_data.seasons import Season

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

print(env_file)
raw_data_dir  = parsed_dotenv["phytooracle_data"]

class RGB_Ind_Images(object):
    """
    from phytooracle_data.rgb_ind_images import RGB_Ind_Images
    rgb = RGB_Ind_Images(season=10)
    """

    def __init__(self, season=None, force_download=False, number_plants=5):
        
        """
        /iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_4/season10_individual_plants_2021-05-17.tar.gz
        """

        if season is not None:
            self.season = Season(season=season)
        else:
            log.critical(f"You must provide {self.__class__} with a season or start and end dates")
            sys.exit(0)


        # Figure out if we need to download the data.
        need_to_download_data = False
        rgb_images_filename = 'season10_individual_plants_2021-05-17.tar.gz'
        season_dir_name = self.season.name()
        rgb_data_rawdir = os.path.join(raw_data_dir, season_dir_name)
        rgb_data_filepath = os.path.join(rgb_data_rawdir, rgb_images_filename)

        if not os.path.isfile(rgb_data_filepath):
            # Data doesn't exist locally
            log.info(f"Didn't find {rgb_data_filepath}, fetching it with irods...")
            need_to_download_data = True
        if force_download:
            if not need_to_download_data:
                # Data exists locally, but we're going to overwrite it.
                log.info(f"Found local rgb data, but we've been asked to re-download it with the force_download flag")
                need_to_download_data = True

        if need_to_download_data:
            os.makedirs(rgb_data_rawdir, exist_ok=True)
            import shutil
            if shutil.which('iget') is None:
                log.critical(f"You need to install irods so we can fetch the data")
                sys.exit(0)
            import subprocess
            # iget -N 0 -PVT /path/to/file
            irods_path = f"/iplant/home/shared/phytooracle/{self.season.name()}/level_4/season10_individual_plants_2021-05-17.tar.gz"
            result = subprocess.run(["iget", "-N", "0", "-rKPVT", irods_path])
            if result.returncode != 0:
                log.critical(f"iget did not complete successfully... {result}")
                sys.exit(0)
            shutil.move(rgb_images_filename, rgb_data_filepath)

            # Untarring the individual plants tar file
            
            result = subprocess.run(["tar", "-xvf", rgb_data_filepath, "-C", rgb_data_rawdir])
            if result.returncode != 0:
                log.critical(f"untaring did not complete successfully... {result}")
                sys.exit(0)

        list_pred_dates = self.season.dict['yield_prediction_dates']['rgb']
        print(list_pred_dates)

        images_dict = {}
        list_folders = os.listdir(os.path.join(rgb_data_rawdir,rgb_images_filename.replace(".tar.gz","")))

        for f in list_folders:
            
            single_image_files = os.listdir(os.path.join(rgb_data_rawdir,rgb_images_filename.replace(".tar.gz",""),f))
            list_available_dates = [file.replace("_ortho_10pct_cubic.tif","") for file in single_image_files]
            all_pred_dates_available =  all(elem in list_available_dates for elem in list_pred_dates)

            # print('--------------------------')
            # print(list_available_dates)
            # print(list_pred_dates)
            # print(all_pred_dates_available)
            # print('--------------------------')
            
            if not all_pred_dates_available:
                continue
            
            files_by_date = {}

            for l in list_pred_dates:
                files_by_date[l] = os.path.join(rgb_data_rawdir,rgb_images_filename.replace(".tar.gz",""),f,"{0}_ortho_10pct_cubic.tif".format(l))
            

            splitted = f.split("_")
            range_column = splitted[-1]
            
            if range_column not in images_dict:
                images_dict[range_column] = [files_by_date]
            else:
                images_dict[range_column].append(files_by_date)
            

        complete_images_dict = {}

        for k in images_dict:
            if len(images_dict[k])<5:
                continue
            else:
                complete_images_dict[k] = images_dict[k][:5]
            
        self.images_sequences = complete_images_dict
            
            