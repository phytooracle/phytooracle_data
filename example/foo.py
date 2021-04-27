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

import phytooracle_data.azmet as azmet
AZMet = azmet.AZMet(season=10)

print(AZMet.daily_df)
print(AZMet.hourly_df)
print(AZMet.eto_df)
print(AZMet.hu_df)

##################################################
#                Seasons Example                 #
##################################################

import pprint
import phytooracle_data.seasons as seasons
s10 = seasons.Season(season=10)
pprint.pprint(s10.dict)
print()
pprint.pprint(s10.years())
print()
pprint.pprint(seasons.Season(season=12).name())

"""
rgb = data.rgb.RGB(season=10)
df = rgb.df[ rgb.df.double_lettuce == 0 ]
df.groupby(by='treatment').max.bounding_area_m2

biggest_plant_idx = rgb.df.bounding_area_m2.idxmax()
biggest_plant_name = rgb.df.iloc[ biggest_plant_idx ].plant_name

#rgb_images_of_biggest_plant = rgb.get_images_of_plant(biggest_plant_name)
#
#fig, ax
#for img in rgb_images_of_biggest_plant:
"""
