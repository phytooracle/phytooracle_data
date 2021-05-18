import sys

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)

import dotenv
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)
parsed_dotenv = dotenv.dotenv_values()
raw_data_dir  = parsed_dotenv["raw_data_dir"]
phytooracle_data_library_path  = parsed_dotenv["phytooracle_data_library_path"]

sys.path.append(phytooracle_data_library_path)

##################################################
#                 AZMet Example                  #
##################################################

from phytooracle_data.azmet import AZMet
azmet = AZMet(season=10)

print(azmet.daily_df)
print(azmet.hourly_df)
print(azmet.eto_df)
print(azmet.hu_df)

##################################################
#                Seasons Example                 #
##################################################

import pprint
from phytooracle_data.seasons import Season
s10 = Season(season=10)
pprint.pprint(s10.dict)
print()
pprint.pprint(s10.years())
print()
pprint.pprint(seasons.Season(season=12).name())

##################################################
#                  RGB Example                   #
##################################################

from phytooracle_data.rgb import RGB_Data
rgb = RGB_Data(season=10)
no_double_lettuce_df = rgb.df[ rgb.df.double_lettuce == 0 ]
treatment_1_no_lettuce_df = no_double_lettuce_df[ no_double_lettuce_df.treatment == 'treatment 1' ]

print("All Plants...")
print("Number of observations by date")
print(rgb.number_observations_by_date())
print("Treatment 1 / no doubles...")
print("Number of observations by date")
print(rgb.number_observations_by_date(df=treatment_1_no_lettuce_df))

print("All Plants...")
print("Number of plants with n observations")
print(rgb.number_plants_with_n_observations())
print("Treatment 1 / no doubles...")
print("Number of plants with n observations")
print(rgb.number_plants_with_n_observations(df=treatment_1_no_lettuce_df))

rgb.plot_number_observations_vs_date_per_column('treatment')
rgb.plot_number_observations_vs_date_per_column('double_lettuce')

# Print biggest plants from three treatments
rgb.df.groupby(by='treatment').max().bounding_area_m2

# Find biggest plant
biggest_plant_idx = rgb.df.bounding_area_m2.idxmax()
biggest_plant_name = rgb.df.iloc[ biggest_plant_idx ].plant_name
print(f"Biggest plant: {biggest_plant_name}")

# Find biggest plant that's not a double...
biggest_plant_idx = no_double_lettuce_df.bounding_area_m2.idxmax()
biggest_plant_name = no_double_lettuce_df.iloc[ biggest_plant_idx ].plant_name
print(f"Biggest single lettuce plant: {biggest_plant_name}")

#rgb_images_of_biggest_plant = rgb.get_images_of_plant(biggest_plant_name)
#
#fig, ax
#for img in rgb_images_of_biggest_plant:
#get_images_of_plant(self, plant_name):
