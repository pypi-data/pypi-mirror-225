import pandas as pd
import awswrangler as wr
from .utils import strip_where_from_filter_if_exists


class AthenaColumn:
    def __init__(self, db_name, tbl_name, col_name, time_col='', geo_col='', filter_string="1=1", bin_info={}):
        self.db_name = db_name
        self.tbl_name = tbl_name
        self.col_name = col_name

        self.time_col = time_col
        self.geo_col = geo_col
        self.filter_string = filter_string
        self.bin_info = bin_info

        self.agg_counts = self.get_agg_counts()
        self.bin_counts = self.bin_the_counts()

    def get_agg_counts(self):
        # function to pull counts back from

        cols_to_include = [self.col_name]
        if self.time_col:
            cols_to_include.append(self.time_col)
        if self.geo_col:
            cols_to_include.append(self.geo_col)

        col_list_as_string = ", ".join(cols_to_include)
        optional_where_condition = strip_where_from_filter_if_exists(self.filter_string)

        SQL = f'SELECT {col_list_as_string}, count(1) as "n" from {self.tbl_name} where {optional_where_condition} group by {col_list_as_string} order by n desc'
        return wr.athena.read_sql_query(SQL, self.db_name)

    # ###############################################
    # ### Ordinal binning methods
    # ###############################################

    def apply_fixed_ordinal_bins(self, agg_df, cut_col, left_endpoint_list):
        cutpoints = left_endpoint_list
        # makes sure I cover the values
        if agg_df[cut_col].max() >= cutpoints[-1]:
            cutpoints.append(agg_df[cut_col].max() + 1)

        if agg_df[cut_col].min() < cutpoints[0]:
            cutpoints = [agg_df[cut_col].min()] + cutpoints

        agg_df[cut_col] = pd.cut(agg_df[cut_col], bins=cutpoints, right=False, duplicates='drop', include_lowest=True)
        return agg_df

    def get_ordinal_bin_list_from_agg_distn(self, agg_df, cut_col, num_bins, agg_metric='n'):
        df = agg_df.sort_values(cut_col, ascending=True).copy()
        df['pct_metric'] = df[agg_metric].cumsum() / df[agg_metric].sum()

        # figure out bin spacing... convert to percentile
        bin_width = 1 / num_bins
        pctiles_to_search = [i * bin_width for i in range(num_bins)][1:]

        # start building the bin list
        new_bin_list = []

        # if -1 exists... it's in the bin.
        if df[cut_col].min() < 0:
            new_bin_list.append(-1)

        # min non-negative value is a bin as well
        init_non_negative = df.query(f"{cut_col} >= 0").iloc[0]
        init_bin = init_non_negative[cut_col]
        new_bin_list.append(init_bin)
        init_pct = init_non_negative['pct_metric']

        # beyond this... look for min value GTE pctiles
        cum_pct_found = init_pct
        for pct in pctiles_to_search:
            if pct < cum_pct_found:
                print(f"skip {pct} since I already have {cum_pct_found}")
            else:
                new_bin_row = df.query(f"pct_metric >= {pct}").iloc[0]
                new_bin_list.append(new_bin_row[cut_col])
                cum_pct_found = new_bin_row['pct_metric']

        return new_bin_list

    # ###############################################
    # ### Ordinal categorical methods
    # ###############################################

    def apply_fixed_categorical_bins(self, agg_df, cut_col, stand_alone_value_list, fallback_val='@Other'):
        agg_df.loc[~agg_df[cut_col].isin(stand_alone_value_list), cut_col] = fallback_val
        return agg_df

    def get_categorical_bin_list_from_agg_distn(self, agg_df, cut_col, agg_metric='EExp', agg_metric_pct_thresh=0.03):
        tmp_agg = agg_df.groupby(cut_col)[[agg_metric]].sum().reset_index()
        tmp_agg['pct'] = tmp_agg[[agg_metric]] / tmp_agg[[agg_metric]].sum()
        return tmp_agg.query(f"pct > {agg_metric_pct_thresh}")[cut_col].tolist()

    # ###############################################
    # ### Ordinal categorical methods
    # ###############################################

    def _handle_var_info(self, df, var_info):
        if var_info['ord_cat'] == 'ord':
            if var_info['bin_strategy'] == 'process':
                bin_list = self.get_ordinal_bin_list_from_agg_distn(df, var_info['name'], var_info['bin_parameter'],
                                                                    agg_metric='n')
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'fixed':
                bin_list = var_info['bin_parameter']
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'top':
                top_vals = var_info['bin_parameter']
                bin_list = df.groupby(var_info['name'])['n'].sum().reset_index().sort_values('n', ascending=False)[
                               var_info['name']].tolist()[:top_vals]
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list, fallback_val=-999)
        elif var_info['ord_cat'] == 'cat':
            if var_info['bin_strategy'] == 'process':
                bin_list = self.get_categorical_bin_list_from_agg_distn(df, var_info['name'], agg_metric='n',
                                                                        agg_metric_pct_thresh=var_info['bin_parameter'])
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'fixed':
                bin_list = var_info['bin_parameter']
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'top':
                top_vals = var_info['bin_parameter']
                bin_list = df.groupby(var_info['name'])['n'].sum().reset_index().sort_values('n', ascending=False)[
                               var_info['name']].tolist()[:top_vals]
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
        return df

    def bin_the_counts(self):
        binned_df = self.agg_counts.copy()
        for col_name, col_config in self.bin_info.items():
            if col_config['ord_cat'] == 'ord':
                print(f"convert {col_name} to float")
                binned_df = binned_df.astype({col_name: float})
            binned_df = self._handle_var_info(binned_df, col_config)

        return binned_df.groupby(binned_df.columns.tolist()[:-1])['n'].sum().reset_index()
