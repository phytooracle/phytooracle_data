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
            [2020-03-02,  # Say why this is anomalous
            2020-02-08]  # Bad Ortho
    complete_field_dates:
        rgb:
            ['2020-01-14',
            '2020-01-18',
            '2020-01-21',
            '2020-01-28',
            #'2020-01-29',
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
            ['2021-05-24__11-24-18-691_sorghum',
            '2021-05-27__11-15-48-347_sorghum',
            '2021-05-31__09-45-51-244_sorghum',
            '2021-06-01__13-35-09-588_sorghum',
            '2021-06-03__09-45-48-820_sorghum',
            '2021-06-03__13-10-35-405_sorghum',
            '2021-06-07__09-48-18-689_sorghum',
            '2021-06-10__09-50-47-774_sorghum',
            '2021-06-10__11-51-08-761_sorghum',
            '2021-06-14__09-40-04-974_sorghum',
            '2021-06-17__09-44-36-859_sorghum',
            '2021-06-17__11-53-33-303_sorghum',
            '2021-06-17__20-00-27-279_sorghum',
            '2021-06-21__11-18-51-429_sorghum',
            '2021-06-28__09-48-48-828_sorghum',
            '2021-06-28__13-01-20-180_sorghum',
            '2021-07-01__09-38-10-913_sorghum',
            '2021-07-01__11-27-27-947_sorghum',
            '2021-07-05__09-30-37-389_sorghum',
            '2021-07-05__13-33-08-376_sorghum',
            '2021-07-08__09-42-43-087_sorghum',
            '2021-07-08__11-35-00-942_sorghum',
            '2021-07-12__09-41-47-119_sorghum',
            '2021-07-12__11-59-46-678_sorghum',
            '2021-07-14__13-18-15-383_sorghum',
            '2021-07-15__09-45-31-924_sorghum',
            '2021-07-19__09-45-47-968_sorghum',
            '2021-07-19__11-30-47-821_sorghum',
            '2021-07-21__09-45-49-078_sorghum',
            '2021-07-21__11-30-47-527_sorghum',
            '2021-07-27__09-45-48-326_sorghum',
            '2021-07-27__11-30-47-477_sorghum',
            '2021-07-29__09-18-39-727_sorghum',
            '2021-07-29__11-09-49-955_sorghum',
            '2021-08-02__09-27-23-287_sorghum',
            '2021-08-02__13-11-38-442_sorghum',
            '2021-08-06__09-11-41-095_sorghum',
            '2021-08-06__13-01-51-673_sorghum',
            '2021-08-10__09-51-53-542_sorghum',
            '2021-08-10__11-50-39-482_sorghum',
            '2021-08-16__09-30-36-051_sorghum',
            '2021-08-16__11-18-53-712_sorghum',
            '2021-08-23__09-59-11-223_sorghum',
            '2021-08-23__13-44-17-353_sorghum',
            '2021-08-30__09-06-10-001_sorghum',
            '2021-08-31__08-22-21-401_sorghum',
            '2021-09-06__09-05-16-165_sorghum',
            '2021-09-06__12-04-25-881_sorghum',
            '2021-09-10__09-07-30-732_sorghum',
            '2021-09-11__10-28-04-504_sorghum',
            '2021-09-13__09-15-54-124_sorghum',
            '2021-09-13__12-50-44-622_sorghum',
            '2021-10-18__10-00-56-076_sorghum',
            '2021-10-21__10-07-55-141_sorghum',
            '2021-10-25__10-03-56-660_sorghum',
            '2021-10-28__09-48-26-814_sorghum']

13:
    name: season_13_lettuce_yr_2022
    start_date: 2022-11-14
    end_date: 2023-03-30
    flir_temp_units: "C"
    complete_field_dates:
            rgb:
                ['2022-01-27__10-54-27-164_lettuce',
                '2022-01-31__10-45-39-463_lettuce',
                '2022-02-01__10-39-38-575_lettuce',
                '2022-02-04__10-42-09-085_lettuce',
                '2022-02-07__10-33-28-355_lettuce',
                '2022-02-08__10-38-14-413_lettuce',
                '2022-02-09__10-42-41-102_lettuce',
                '2022-02-10__10-37-53-213_lettuce',
                '2022-02-11__10-37-09-800_lettuce',
                '2022-02-14__10-41-53-763_lettuce',
                '2022-02-16__10-43-57-766_lettuce',
                '2022-02-17__10-39-08-670_lettuce',
                '2022-02-18__10-41-21-294_lettuce',
                '2022-02-21__10-38-28-308_lettuce',
                '2022-02-25__10-39-57-210_lettuce',
                '2022-02-28__10-38-14-633_lettuce',
                '2022-03-02__10-56-11-405_lettuce',
                '2022-03-07__10-38-37-481_lettuce',
                '2022-03-09__10-40-08-384_lettuce',
                '2022-03-11__10-39-22-200_lettuce',
                '2022-03-15__11-12-27-310_lettuce']

14:
    name: season_14_sorghum_yr_2022
    start_date: 2022-04-23
    end_date: 2022-08-19
    flir_temp_units: "C"
    complete_field_dates:
            rgb:
                ['2022-05-06__10-36-03-370_sorghum',
                '2022-05-09__10-38-40-876_sorghum',
                '2022-05-10__10-40-54-537_sorghum',
                '2022-05-11__10-38-14-929_sorghum',
                '2022-05-11__13-39-26-313_sorghum',
                '2022-05-12__10-38-48-237_sorghum',
                '2022-05-13__10-39-57-060_sorghum',
                '2022-05-17__10-43-23-134_sorghum',
                '2022-05-18__10-39-10-247_sorghum',
                '2022-05-19__10-34-42-254_sorghum',
                '2022-05-20__10-36-30-414_sorghum',
                '2022-05-23__10-40-17-118_sorghum',
                '2022-05-24__10-40-51-950_sorghum',
                '2022-05-25__10-43-34-713_sorghum',
                '2022-05-26__10-40-55-294_sorghum',
                '2022-05-27__10-39-10-543_sorghum',
                '2022-05-31__11-08-15-183_sorghum',
                '2022-06-01__10-40-28-979_sorghum',
                '2022-06-02__11-55-07-609_sorghum',
                '2022-06-03__10-43-08-401_sorghum',
                '2022-06-06__10-43-37-538_sorghum',
                '2022-06-07__10-42-53-271_sorghum',
                '2022-06-08__10-40-59-925_sorghum',
                '2022-06-09__10-56-13-313_sorghum',
                '2022-06-10__10-37-47-617_sorghum',
                '2022-06-13__10-37-59-152_sorghum',
                '2022-06-15__10-40-03-270_sorghum',
                '2022-06-16__10-37-27-226_sorghum',
                '2022-06-17__10-40-40-763_sorghum',
                '2022-06-20__10-39-29-339_sorghum',
                '2022-06-21__10-39-44-724_sorghum',
                '2022-06-22__10-38-49-594_sorghum',
                '2022-06-27__10-38-42-820_sorghum',
                '2022-06-28__10-38-01-694_sorghum',
                '2022-06-29__10-37-48-734_sorghum',
                '2022-06-30__10-41-53-947_sorghum',
                '2022-07-01__10-38-00-426_sorghum',
                '2022-07-04__10-41-07-090_sorghum',
                '2022-07-05__11-55-04-715_sorghum',
                '2022-07-07__10-44-23-322_sorghum',
                '2022-07-08__10-40-06-715_sorghum',
                '2022-07-11__10-40-50-669_sorghum',
                '2022-07-12__10-46-48-940_sorghum',
                '2022-07-13__10-38-53-412_sorghum',
                '2022-07-18__11-28-30-829_sorghum',
                '2022-07-19__10-39-15-167_sorghum',
                '2022-07-20__10-41-02-753_sorghum',
                '2022-07-21__10-41-51-272_sorghum',
                '2022-07-22__10-39-55-879_sorghum',
                '2022-07-25__10-39-09-601_sorghum',
                '2022-07-26__10-42-21-528_sorghum',
                '2022-07-27__10-43-32-175_sorghum',
                '2022-07-28__10-40-09-387_sorghum',
                '2022-07-29__10-59-53-765_sorghum',
                '2022-08-01__10-38-54-805_sorghum',
                '2022-08-05__10-37-48-961_sorghum',
                '2022-08-08__10-36-27-581_sorghum',
                '2022-08-11__10-42-38-382_sorghum',
                '2022-08-11__13-45-35-458_sorghum',
                '2022-08-12__10-39-22-016_sorghum',
                '2022-08-15__10-41-22-100_sorghum',
                '2022-08-18__10-44-16-814_sorghum',
                '2022-08-19__10-42-50-612_sorghum']
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
