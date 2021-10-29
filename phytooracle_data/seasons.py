import yaml
import pandas as pd

import logging
logging.basicConfig(
    level=logging.INFO,
    #format='%(levelname)s - %(asctime)s - %(module)s - %(message)s',
)
log = logging.getLogger(__name__)

season_config_yaml = """
10:
    name: season_10_lettuce_yr_2020
    start_date: 2019-12-01
    end_date: 2020-03-04
    flir_temp_units: "K"
    anomalous_dates:
        rgb:
            2020-03-02  # Say why this is anomalous
            2020-02-08  # Bad Ortho
    complete_field_dates:
        rgb:
            ['2020-01-14',
            '2020-01-18',
            '2020-01-20',
            '2020-01-28',
            '2020-01-29',
            '2020-01-31',
            '2020-02-03',
            #'2020-02-08',
            '2020-02-15',
            '2020-02-18',
            '2020-03-01',
            '2020-03-03']
    yield_prediction_dates:
        rgb:
            ['2020-01-14',
            '2020-01-18',
            '2020-01-28',
            '2020-01-31',
            '2020-02-03',
            '2020-02-15',
            '2020-02-18']
12:
    name: season_12_sorghum_soybean_sunflower_tepary_yr_2021
    start_date: 2021-04-01
    end_date: 2021-09-09
    flir_temp_units: "C"
"""

seasons_dict = yaml.safe_load(season_config_yaml)

class Season(object):
    """
    ils /iplant/home/shared/phytooracle/
    """

    def __init__(self, season=None):
        if season is None:
            log.critial(f"You must provide {self.__class__} with a season")
            return None

        # Is requested season an integer or a string?  (e.g. 9 vs season_9_sorghum_yr_2019)
        if type(season) is not int:
            requested_season_number = 0     # We'll either replace this, or find it doesn't exist later
            for n, season_info in seasons_dict.items():
                if season_info['name'] == season:
                    requested_season_number = n
                    break
        else:
            requested_season_number = season

        # Does requested season number exist?
        if type(requested_season_number) is int:
            if requested_season_number not in seasons_dict.keys():
                log.critical(f"Requested season ({season}) does not exist")
                return None

        # We have a valid season!
        self.season_number = requested_season_number
        self.dict = seasons_dict[self.season_number]

    def years(self):
        return list(range(self.dict['start_date'].year, self.dict['end_date'].year + 1))

    def name(self):
        return self.dict['name']
    def start_date(self):
        return pd.to_datetime(self.dict['start_date'])
    def end_date(self):
        return pd.to_datetime(self.dict['end_date'])
