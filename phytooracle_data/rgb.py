import os.path
import pdb
import glob
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from data.seasons import Season

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)

# Deal with local machine paths, etc.
import dotenv
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)
parsed_dotenv = dotenv.dotenv_values()
project_dir = os.path.dirname(env_file)
data_dir    = parsed_dotenv["data_dir"]
raw_data_dir    = parsed_dotenv["raw_data_dir"]

class RGB(object):
    """
    import data.rgb
    rgb = data.rgb.RGB(season=10)
    rgb.df.iloc[0]
    """

    def __init__(self, season=10, force_download=False, remove_anomalous_dates=True):
        
        """
        /iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_3/stereoTop/season10_plant_clustering/stereoTop_full_season_clustering.csv
        """

        self.season_label = Season.season_names[season]

        download_data = False
        rgb_data_filename = 'stereoTop_full_season_clustering.csv'
        season_dir_name = self.season_label
        rgb_data_rawdir = os.path.join(raw_data_dir, season_dir_name)
        rgb_data_filepath = os.path.join(rgb_data_rawdir, rgb_data_filename)

        if not os.path.isfile(rgb_data_filepath):
            # Data doesn't exist locally
            log.info(f"Didn't find {rgb_data_filepath}, fetching it with irods...")
            download_data = True
        if force_download:
            if not download_data:
                # Data exists locally, but we're going to overwrite it.
                log.info(f"Found local rgb data, but we've been asked to re-download it with the force_download flag")
                download_data = True

        if download_data:
            os.makedirs(rgb_data_rawdir, exist_ok=True)
            import shutil
            if shutil.which('iget') is None:
                log.error(f"You need to install irods so we can fetch the data")
            import subprocess
            # iget -N 0 -PVT /path/to/file
            irods_path = f"/iplant/home/shared/phytooracle/{season_dir_name}/level_3/stereoTop/season10_plant_clustering/stereoTop_full_season_clustering.csv"
            result = subprocess.run(["iget", "-N", "0", "-PVT", irods_path])
            if result.returncode != 0:
                log.error(f"iget did not complete successfully... {result}")
            shutil.move(rgb_data_filename, rgb_data_filepath)
            

        logging.info(f"Reading RGB data from {rgb_data_filepath}")
        df = pd.read_csv(rgb_data_filepath)
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        if remove_anomalous_dates:
            self.anomalous_dates = Season.anomalous_dates[self.season_label]['rgb']
            df = df[ ~df.date.isin(self.anomalous_dates) ]

        #rgb_df  = rgb_df.melt( id_vars=["plant_name","plot"], var_name='date', value_name='rgb')
        #flir_df = flir_df.melt(id_vars=["plant_name","plot"], var_name='date', value_name='flir')

        df['date']  = df['date'].astype(np.datetime64)
        self.df = df

    def get_images_of_plant(self, plant_name):
        path_to_images = '/media/equant/7fe7f0a0-e17f-46d2-82d3-e7a8c25200bb/work/stereoTop/ind_plant_images'
        plant_image_paths = glob.glob(os.path.join(path_to_images, plant_name))
        return plant_image_paths

    def number_observations_by_date(self):
        if not hasattr(self, 'n_obs_by_date'):
            self.n_obs_by_date = self.df.groupby(by='date').size()
        return self.n_obs_by_date
        pass

    def number_sequences(self):
        plants = rgb.df.groupby(by='plant_name')
        if not hasattr(self, 'n_obs_by_date'):
            self.n_obs_by_date = self.df.groupby(by='date').size()
        return self.n_obs_by_date
        pass

    def plot_n_observations_vs_date_per_column(self, column_name):
        if column_name in self.df.columns:
            self.df.groupby(by=[column_name,'date']).size().unstack().T.plot()
            plt.show()
        else:
            log.warning(f"Can not plot_n_observations_vs_date_per_column with column: {column_name}")


"""
# Figure
dates.size().plot(title="Season 10 #Plants w/ RGB", xlabel="date", ylabel="# Plants")
plt.savefig(os.path.join(reports_dir, "n_plants_vs_date.pdf"))
plt.savefig(os.path.join(reports_dir, "n_plants_vs_date.png"))

sequence_length = plants.size().max() 
scan_days = plants.size()
plants_with_sequence_length_scans = scan_days[scan_days == sequence_length]
"""
