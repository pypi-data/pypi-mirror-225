import pandas as pd


def default_agg_fcn(df):
    agg_dict = {
        'rec_count': df.shape[0],
    }
    return pd.Series(agg_dict)[['rec_count']]


def convert_to_distn_in_cols(counts_df, sec_var, col):
    tmp_df = counts_df.pivot(index=col, columns=sec_var, values='rec_count')  # reshape the counts
    tmp_df.columns = tmp_df.columns.tolist()  # make columns single level (pivot added some junk)
    tmp_df = tmp_df.div(tmp_df.sum(axis=0), axis=1).fillna(0)  # convert to percentages within columns
    return tmp_df.reset_index()  # reset the index when passing back
