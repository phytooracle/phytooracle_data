import sys, os
#import os.path
#import pdb
#import glob
#import urllib.request
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from datetime import datetime
import subprocess

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)



def get_data(local_path, irods_path, force_download=False):

    need_to_download_data = False # Prove me wrong
    saved_working_directory = os.getcwd()

    if not os.path.isfile(local_path):
        # Data doesn't exist locally
        log.info(f"Didn't find {local_path}, fetching it with irods...")
        need_to_download_data = True
    if force_download:
        if not need_to_download_data:
            # Data exists locally, but we're going to overwrite it.
            log.info(f"Found local data, but we've been asked to re-download it with the force_download flag")
            need_to_download_data = True

    if need_to_download_data:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        import shutil
        if shutil.which('iget') is None:
            log.critical(f"You need to install irods so we can fetch the data")
            sys.exit(0)
        # iget -N 0 -PVT /path/to/file
        os.chdir(os.path.dirname(local_path))
        result = subprocess.run(["iget", "-N", "0", "-PVT", irods_path])
        if result.returncode != 0:
            log.critical(f"iget did not complete successfully... {result}")
            sys.exit(0)
        os.chdir(saved_working_directory)
    return True


def date_is_between(date, start_date, end_date):
    if date <= end_date:
        if date >= start_date:
            return True
    return False

def find_nearest_date(list_of_dates, target_date):
    if type(list_of_dates[0]) is str:
        import datetime
        datetime_format_string="%Y-%m-%d"
        list_of_dates = [datetime.datetime.strptime(x, datetime_format_string) for x in list_of_dates]
    if type(target_date) is str:
        import datetime
        datetime_format_string="%Y-%m-%d"
        target_date = datetime.datetime.strptime(target_date, datetime_format_string)

    nearest_date = min(list_of_dates, key=lambda x: abs(x-target_date))
    #print(list_of_dates)
    #print(target_date)
    #print(nearest_date)
    return nearest_date

def find_common_dates_between_sensors(I1, I2, threshold=2, datetime_format_string="%Y-%m-%d"):
    """
    Loop through I1 and look for matching dates in I2 that are within threshold days.
    If there's an exact match use that.
    If there are multiple matches, use the closest.
    If there are multiple closest matches, use the last one.

    threshold is in days.

    exact matches only if threshold is zero.
    """
    import datetime

    if len(I1.dates) == 0:
        I1.get_dates()
    if len(I2.dates) == 0:
        I2.get_dates()

    if threshold == 0:
        # Only want exact matches, so return 1to1 mapping
        I1_list = list(set(I1.dates) & set(I2.dates))
        I2_list = list(set(I1.dates) & set(I2.dates))
        return I1_list, I2_list

    I1_datetimes = [datetime.datetime.strptime(x, datetime_format_string) for x in I1.dates]
    I2_datetimes = [datetime.datetime.strptime(x, datetime_format_string) for x in I2.dates]

    # This is what we'll be returning at the end
    I1_list = []
    I2_list = []

    # Loop through I1 +/- threshold, and see which times from I2 are within the date range
    for _idx, target_date in enumerate(I1_datetimes):
        if target_date in I2_datetimes:
            # Exact match, so take that.
            matching_date = target_date
        else:
            earliest_date = target_date - datetime.timedelta(days=threshold)
            latest_date   = target_date + datetime.timedelta(days=threshold)
            valid_dates = [x for x in I2_datetimes if date_is_between(x, earliest_date, latest_date)]
            if len(valid_dates) == 0:
                # No match, start loop over.
                continue
            matching_date = find_nearest_date(valid_dates, target_date)
        I1_list.append(target_date.strftime(datetime_format_string))
        I2_list.append(matching_date.strftime(datetime_format_string))


    #I1_list = list(set(I1.dates) & set(I2.dates))
    #I2_list = list(set(I1.dates) & set(I2.dates))
    return I1_list, I2_list


# Everything above this line is the right way to do things
###########################################################################################
# Everything above this line is not and may not work anymore.


def get_images_of_plant(plant_name):
    path_to_images = '/media/equant/7fe7f0a0-e17f-46d2-82d3-e7a8c25200bb/work/stereoTop/ind_plant_images'
    plant_image_paths = glob.glob(os.path.join(path_to_images, plant_name))
    return plant_image_paths

def number_observations_by_date(df):
    return df.groupby(by='date').size()
    pass

def number_plants_with_n_observations(df):
    """
    How many plants have 13 total observations?  How many have 17?
    returns a list of n, and how many plants have n observations.
    """
    return df.groupby(by='plant_name').size().value_counts().sort_index()

def plot_number_observations_vs_date_per_column(column_name):
    """
    I think this should go into a visualization class.  I dont think we should
    do this [NPH].  Leaving it here for reference.
    """
    if column_name in df.columns:
        if type(column_name) is list:
            # multiple columns passed to us
            df.groupby(by=column_name+['date']).size().unstack().T.plot()
        else:
            # only one column passed to us
            df.groupby(by=[column_name,'date']).size().unstack().T.plot()
        plt.show()
    else:
        log.warning(f"Can not plot_n_observations_vs_date_per_column with column: {column_name}")


def return_plants_with_at_least_n_observations(filtered_df, min_n):
    all_plants = filtered_df.groupby(by='plant_name')
    all_plants_with_at_least_n_obs = all_plants.size()[ all_plants.size() > min_n ]
    filtered_df = filtered_df[filtered_df.plant_name.isin(all_plants_with_at_least_n_obs.index)]
    assert len(filtered_df.plant_name.unique()) == len(all_plants_with_at_least_n_obs), "Nathan screwed something up!"
    return filtered_df

