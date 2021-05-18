
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
