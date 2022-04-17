import sys
import os.path
import os
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

    def initialize_paths(self):
        self.pipeline_preprocessing_dir_to_use = "preprocessing"

    def get_dates(self):
        
        if len(self.file_list) == 0:
            self.get_file_list()
        if self.season.season_number == 10:
            wanted_files = [x.replace("  C- ", "") for x in self.file_list if len(x.split("/")[-1].split("-")) == 3]
        if self.season.season_number == 11:
            wanted_files = [x.replace("  C- ", "") for x in self.file_list if len(x.split("/")[-1].split("-")) == 3]
        elif self.season.season_number == 12:
            wanted_files = [x.replace("  C- ", "") for x in self.file_list if len(x.split("/")[-1].split("-")) == 6]

        self.dates = [x.split("/")[-1] for x in wanted_files]
        return self.dates

    def download_untar_heatmap_for_date(self,use_date):
        
        heatmap_tar_filename = f"{use_date}_heat_map.tar"
        irods_path = os.path.join(self.irods_base_data_path(),use_date, heatmap_tar_filename)
        local_path = os.path.join(self.local_base_data_path(), heatmap_tar_filename)
        
        get_data(local_path, irods_path)
        
        if not os.path.exists(os.path.join(self.local_base_data_path(),"heatmap_out")):

            result = subprocess.run(["tar", "-xvf", local_path, "-C", self.local_base_data_path()])
            if result.returncode != 0:
                log.critical(f"untaring did not complete successfully... {result}")
                sys.exit(0)

        return os.path.join(self.local_base_data_path(),"heatmap_out")


    def irods_preprocessing_path(self, scan_date):
        if self.season.season_number == 10:
            return os.path.join(self.irods_base_data_path(),scan_date,self.pipeline_preprocessing_dir_to_use)
        elif self.season.season_number == 11:
            run_result = subprocess.run(["ils", os.path.join(self.irods_base_data_path())], stdout=subprocess.PIPE).stdout
            lines = run_result.decode('utf-8').splitlines()
            line = [l.split('/')[-1] for l in lines if scan_date in l]
            date_timestamp = line[0]
            return os.path.join(self.irods_base_data_path(),date_timestamp,self.pipeline_preprocessing_dir_to_use)
        elif self.season.season_number == 12:
            return os.path.join(self.irods_base_data_path(),"manual_approach",scan_date,self.pipeline_preprocessing_dir_to_use)

    def local_preprocessing_path(self, scan_date):
        return os.path.join(self.local_base_data_path(),scan_date,self.pipeline_preprocessing_dir_to_use)
    def irods_preprocessing_transformation_json_file_path(self, scan_date):
        return os.path.join(self.irods_base_data_path(),scan_date, "transfromation.json")
    def local_preprocessing_transformation_json_file_path(self, scan_date):
        return os.path.join(self.local_base_data_path(),scan_date, "transfromation.json")


    def get_preprocessed_downsampled_merged_for_date(self,scan_date):
        
        if (self.pipeline_preprocessing_dir_to_use == 'preprocessing'):
            tar_filename = f"{scan_date}_merged_downsampled_preprocessed.tar"
        elif (self.pipeline_preprocessing_dir_to_use == 'alignment'):
            tar_filename = f"{scan_date}_merged_downsampled_aligned.tar"
            tar_filename = f"{scan_date}_west_downsampled.tar"
        else:
            log.critical(f"Can't get_preprocessed_downsampled_merged_for_date() because of unknown pipeline_preprocessing_dir_to_use value: {result}")

        local_working_dir = os.path.join(self.local_preprocessing_path(scan_date))

        irods_path_to_tar = os.path.join(self.irods_preprocessing_path(scan_date), tar_filename)
        local_path_to_tar = os.path.join(local_working_dir, tar_filename)
        
        if not os.path.exists(os.path.join(local_working_dir, "merged_downsampled")):
            get_data(local_path_to_tar, irods_path_to_tar)
            result = subprocess.run(["tar", "-xvf", local_path_to_tar, "-C", local_working_dir])
            if result.returncode != 0:
                log.critical(f"untaring did not complete successfully... {result}")
                sys.exit(0)
            if os.path.exists(local_path_to_tar):
                  os.remove(local_path_to_tar)

        return os.path.join(local_working_dir, "merged_downsampled")
    
    def get_preprocessed_metadata_for_date(self,scan_date):
        
        if (self.pipeline_preprocessing_dir_to_use == 'preprocessing'):
            tar_filename = f"{scan_date}_metadata_preprocessed.tar"
        elif (self.pipeline_preprocessing_dir_to_use == 'alignment'):
            tar_filename = f"{scan_date}_metadata_aligned.tar"

        local_working_dir = self.local_preprocessing_path(scan_date)

        irods_path_to_tar = os.path.join(self.irods_preprocessing_path(scan_date), tar_filename)
        local_path_to_tar = os.path.join(local_working_dir, tar_filename)
        
        
        if not os.path.exists(os.path.join(local_working_dir, "metadata")):
            get_data(local_path_to_tar, irods_path_to_tar)
            result = subprocess.run(["tar", "-xvf", local_path_to_tar, "-C", local_working_dir])
            if result.returncode != 0:
                log.critical(f"untaring did not complete successfully... {result}")
                sys.exit(0)
            if os.path.exists(local_path_to_tar):
                  os.remove(local_path_to_tar)

        return os.path.join(local_working_dir, "metadata")
    
    def upload_transformation_json_file(self, scan_date, local_json_file_path=None):
        """
        This function is used by the Season 10 landmark-mased geocrorection GUI.
        """

        if local_json_file_path is None:
            local_json_file_path = self.local_preprocessing_transformation_json_file_path(scan_date)

        irods_dest = os.path.join(self.irods_preprocessing_path(scan_date), ".")

        result = subprocess.run(["iput", "-fKVPT", local_json_file_path, irods_dest])
        if result.returncode != 0:
            log.critical(f"iput did not complete successfully... {result}")
            sys.exit(0)
            
        print(":: Successfully uploaded to irods.")
        
    def tar_upload_results(self,use_date):
        """
        DEPRECATED
        This is horribly named.
        It was used for the original manual GUI correction
        """

        # folder_path = os.path.join(self.local_base_data_path(),"plant_coords_out")
        tar_path = os.path.join(self.local_base_data_path(),f"{use_date}_plant_coords.tar.gz")
        irods_dest = os.path.join(self.irods_base_data_path(),use_date, ".")

        saved_working_directory = os.getcwd()
        os.chdir(self.local_base_data_path())

        result = subprocess.run(["tar", "-cvf", tar_path, "plant_coords_out"])
        if result.returncode != 0:
            log.critical(f"could not tar the results successfully... {result}")
            sys.exit(0)
        
        os.chdir(saved_working_directory)

        result = subprocess.run(["iput", "-fKVPT", tar_path, irods_dest])
        if result.returncode != 0:
            log.critical(f"iput did not complete successfully... {result}")
            sys.exit(0)
            
        print(":: Successfully uploaded to irods.")
        
