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
    complete_field_dates:
        rgb:
            ['2020-01-14',
            '2020-01-18',
            '2020-01-20',
            '2020-01-28',
            '2020-01-29',
            '2020-01-31',
            '2020-02-03',
            '2020-02-08',
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
11:
    name: season_11_sorghum_yr_2020
    start_date: 2020-10-29
    end_date: 2020-11-07
    flir_temp_units: "K"
    anomalous_dates:
        rgb:
    complete_field_dates:
        rgb:
            ['2020-06-23',
            '2020-06-24',
            '2020-06-25',
            '2020-06-26',
            '2020-06-30',
            '2020-07-02',
            '2020-07-04',
            '2020-07-06',
            '2020-07-07',
            '2020-07-10',
            '2020-07-11',
            '2020-07-12',
            '2020-07-13',
            '2020-07-15',
            '2020-07-16',
            '2020-07-17',
            '2020-07-20',
            '2020-07-22',
            '2020-07-24',
            '2020-07-25',
            '2020-07-26',
            '2020-07-27',
            '2020-07-29',
            '2020-07-31',
            '2020-07-31',
            '2020-07-31',
            '2020-07-31',
            '2020-08-01',
            '2020-08-03',
            '2020-08-05',
            '2020-08-06',
            '2020-08-08',
            '2020-08-10',
            '2020-08-12',
            '2020-08-13',
            '2020-08-15',
            '2020-08-19',
            '2020-08-20',
            '2020-08-22',
            '2020-08-23',
            '2020-08-24',
            '2020-08-31',
            '2020-09-05',
            '2020-09-07',
            '2020-09-12',
            '2020-09-14',
            '2020-09-19',
            '2020-09-21',
            '2020-09-26',
            '2020-09-28',
            '2020-10-03',
            '2020-10-05',
            '2020-10-10',
            '2020-10-12',
            '2020-10-18',
            '2020-10-19',
            '2020-10-24',
            '2020-10-27',
            '2020-10-28',
            '2020-10-29',
            '2020-10-31']
    yield_prediction_dates:
        rgb:
            []
12:
    name: season_12_sorghum_soybean_sunflower_tepary_yr_2021
    start_date: 2021-04-01
    end_date: 2021-09-09
    flir_temp_units: "C"
    complete_field_dates:
        rgb:
            ['2021-08-02__13-11-38-442_sorghum']
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
