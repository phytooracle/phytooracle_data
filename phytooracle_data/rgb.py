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
import shutil

from phytooracle_data.seasons import Season
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

def get_command():
    if shutil.which('iget') is not None:
        return ["iget", "-N", "0", "-PVTK"]
    elif os.path.isfile("/home/equant/bin/gocommands/bin/gocmd"):
        return ["/home/equant/bin/gocommands/bin/gocmd", "get"]
    else:
        log.critical(f"You need to install irods (or gocommands) so we can fetch the data")
        sys.exit(0)


class RGB_Data(object):
    """
    from phytooracle_data.rgb import RGB_Data
    rgb = RGB_Data(season=10)
    df = rgb.df[ rgb.df.double_lettuce == 0 ]
    """

    def __init__(self, season=None, force_download=False, remove_anomalous_dates=True):
        
        """
        /iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_3/stereoTop/season10_plant_clustering/stereoTop_full_season_clustering.csv
        """

        if season is not None:
            self.season = Season(season=season)
        else:
            log.critical(f"You must provide {self.__class__} with a season or start and end dates")
            sys.exit(0)


        # Figure out if we need to download the data.
        need_to_download_data = False
        if self.season.season_number == 10:
            rgb_data_filename = 'stereoTop_full_season_clustering.csv'
        else:
            rgb_data_filename = f'season_{self.season.season_number}_clustering.csv'

        season_dir_name = self.season.name()
        rgb_data_rawdir = os.path.join(raw_data_dir, season_dir_name)
        rgb_data_filepath = os.path.join(rgb_data_rawdir, rgb_data_filename)

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
            # iget -N 0 -PVT /path/to/file
            if self.season.season_number == 10:
                irods_path = f"/iplant/home/shared/phytooracle/{self.season.name()}/level_3/stereoTop/season10_plant_clustering/{rgb_data_filename}"
            else:
                irods_path = f"/iplant/home/shared/phytooracle/{self.season.name()}/level_3/stereoTop/{rgb_data_filename}"
            #result = subprocess.run(["iget", "-N", "0", "-PVTK", irods_path])
            print(f'{" ".join(get_command() + [irods_path])}')
            result = subprocess.run(get_command() + [irods_path])
            if result.returncode != 0:
                log.critical(f"iget did not complete successfully... {result}")
                sys.exit(0)
            shutil.move(rgb_data_filename, rgb_data_filepath)
            

        logging.info(f"Reading RGB data from {rgb_data_filepath}")
        self.rgb_data_filename = rgb_data_filepath
        df = pd.read_csv(rgb_data_filepath)
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        self.anomalous_dates = list(self.season.dict['anomalous_dates'].values())
        if remove_anomalous_dates:
            df = df[ ~df.date.isin(self.anomalous_dates) ]

        #rgb_df  = rgb_df.melt( id_vars=["plant_name","plot"], var_name='date', value_name='rgb')
        #flir_df = flir_df.melt(id_vars=["plant_name","plot"], var_name='date', value_name='flir')

        df['date']  = df['date'].astype(np.datetime64)
        self.df = df


    def calculate_S(self, df):
        if df is None:
            df = self.df

        grouped_plants = df.groupby(by='plant_name')

        for plant_name, plant_row_idxs in grouped_plants.groups.items():
            plant_data = df.loc[plant_row_idxs]
            plant_data['S'] = plant_data.bounding_area_m2 / plant_data.bounding_area_m2.max()
            df.loc[plant_row_idxs, 'S'] = plant_data['S']

        return df


    def make_plot_level_df(self, df):
        if df is None:
            df = self.df
        if 'S' not in df.columns:
            df = self.calculate_S(df)

        plot_df = df.groupby(['plot', 'date']).agg(
                    {
                        'bounding_area_m2' : ['median', 'std'],
                        'S'                : ['median', 'std'],
                        'treatment'        : 'first',
                        'genotype'         : 'first',
                    }
        )
        plot_df.columns = ['bounding_area_m2', 'bounding_area_m2_std', 'S', 'S_std', 'treatment', 'genotype']
        plot_df.reset_index(inplace=True)
        plot_df['plot_name'] = plot_df['plot']
        plot_df['plot'] = plot_df['plot'].str.replace('MAC_Field_Scanner_Season_10_', '')
        plot_df[['range', 'column']] = plot_df['plot'].str.split("_Column_", n=1, expand=True)
        plot_df['range'] = plot_df['range'].str.split('_', expand=True)[1].str.zfill(2)
        plot_df['column'] = plot_df['column'].str.zfill(2)
        plot_df['plot'] = plot_df['range']+plot_df['column']
        return plot_df



"""
# Figure
dates.size().plot(title="Season 10 #Plants w/ RGB", xlabel="date", ylabel="# Plants")
plt.savefig(os.path.join(reports_dir, "n_plants_vs_date.pdf"))
plt.savefig(os.path.join(reports_dir, "n_plants_vs_date.png"))

sequence_length = plants.size().max() 
scan_days = plants.size()
plants_with_sequence_length_scans = scan_days[scan_days == sequence_length]
"""
