import sys, os
import pandas as pd
import numpy as np

import dotenv
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)
parsed_dotenv = dotenv.dotenv_values()
#raw_data_dir  = parsed_dotenv["raw_data_dir"]
phytooracle_data_library_path  = parsed_dotenv["phytooracle_data_library_path"]

sys.path.append(phytooracle_data_library_path)

import phytooracle_data
from phytooracle_data.rgb import RGB_Data
from phytooracle_data.azmet import AZMet

MIN_N_OBS = 10
SEASON = 10

# We will first get our plot info from the rgb data..

rgb = RGB_Data(season=SEASON)
filtered_rgb_df = rgb.df
"""
# If you want to filter out some data, here's a good way to do it...
filtered_rgb_df = filtered_rgb_df.query("double_lettuce == 0")
filtered_rgb_df = filtered_rgb_df.query("treatment != 'border'")
filtered_rgb_df = filtered_rgb_df.query(f"date > '2019-12-20'")
filtered_rgb_df = filtered_rgb_df.query(f"date < '2020-03-03'")
"""

print(f"Working with {len(filtered_rgb_df.plant_name.unique())} plants.")
filtered_rgb_df = phytooracle_data.return_plants_with_at_least_n_observations(filtered_rgb_df, MIN_N_OBS)

# Turn plants into plots
plots_df = rgb.make_plot_level_df(filtered_rgb_df)
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(plots_df['treatment'])
plots_df['treatment_encoded'] = label_encoder.transform(plots_df['treatment'])
