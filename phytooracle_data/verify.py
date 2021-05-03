class Verify(object):
    def all_plots_contain_only_one_genotype(df):
        return df.groupby('plot').genotype.nunique().max() == 1
