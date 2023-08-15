import pandas as pd
import numpy as np
import scipy.stats as scs

# helper functions to process individual variables
def is_numeric_type(s, num_types=['int64', 'float64']):
    if s.dtype in num_types:
        return True
    else:
        return False


def get_distinct_values(s):
    return s.nunique(dropna=False)


def has_missing_values(s):
    if pd.isna(s).sum() > 0:
        return True
    else:
        return False


def create_ordinal_bin_series(s, q=5, missing_bin_label='Missing'):
    qcut_labels = pd.qcut(s, q=q, duplicates='drop').astype(str)  #TODO: how to replace missing without messing up ability to sort in the one-ways downstream?
    qcut_labels[qcut_labels == 'nan'] = missing_bin_label
    qcut_labels.name = f"{s.name}_binned"
    return qcut_labels


def create_categorical_bin_series(s, max_categories=100, other_bin_label='Other-Values'):
    stand_alone_categories = list(s.value_counts().sort_values(ascending=False).iloc[:max_categories].index)
    binned_values = s.copy()
    binned_values.name = f"{s.name}_binned"
    binned_values[~binned_values.isin(stand_alone_categories)] = other_bin_label
    return binned_values


def create_categorical_series_no_missing(s, null_replacement='Missing-Values'):
    new_series = s.fillna(null_replacement).copy()
    new_series.name = f"{s.name}_clean"
    return new_series


def calculate_cramers_v_value(contingency_table):
    # TODO: Guard against blowing up when variables have no one-way stats (i.e. 100% missing values)
    if len(contingency_table) == 1:
        return 0.0
    else:
        try:
            (chi2_stat, p_val, df, expected) = scs.chi2_contingency(contingency_table.values)
        except ValueError:
            return -1
        df_size = contingency_table.sum().sum()
        (df_rows, df_cols) = contingency_table.shape
        if df_rows > df_cols:
            min_dim = df_cols
        else:
            min_dim = df_rows
        return np.sqrt(chi2_stat / df_size / (min_dim - 1))


def sort_df_by_interval_idx(df):
    try:
        df['tmp_idx'] = df.index.astype(str)
        df['tmp_idx'] = df['tmp_idx'].apply(lambda x: float(x.split(',')[0][1:]))
        df.sort_values('tmp_idx', inplace=True)
        df.drop(columns=['tmp_idx'], inplace=True)
        return df
    except:
        return df


class DataframeEda:
    def __init__(self, df, agg_fcn, control_var_list=[], ord_bin_threshold=100, ord_bin_count=5, cat_value_limit=10,
                 calculate_signals=False, signal_weight_col=None, calculate_cramers_v=False,
                 start_with_user_provided_summary_df=False, user_provided_summary_df=None):
        self.df = df
        self.agg_fcn = agg_fcn
        self.control_var_list = control_var_list
        self.ord_bin_threshold = ord_bin_threshold
        self.ord_bin_count = ord_bin_count
        self.cat_value_limit = cat_value_limit
        self.calculate_signals = calculate_signals
        self.signal_weight_col = signal_weight_col
        self.calculate_cramers_v = calculate_cramers_v
        self.start_with_user_provided_summary_df = start_with_user_provided_summary_df
        self.user_provided_summary_df = user_provided_summary_df

        self.control_df_list = self.get_control_total_summaries()
        self.control_binned_series_dict = self.get_control_binned_series_dict()
        self.var_info_dict = self.get_var_info_dict()
        self.var_summary = self.get_var_summary()

    def get_binned_series(self, col):
        # utility function to get the binned/cleaned series.
        if is_numeric_type(self.df[col]):
            if get_distinct_values(self.df[col]) > self.ord_bin_threshold:
                binned_values = create_ordinal_bin_series(self.df[col], q=self.ord_bin_count)
            else:
                binned_values = self.df[col]
                binned_values.name = f"{col}_binned"
        else:
            if get_distinct_values(self.df[col]) > self.cat_value_limit:
                binned_values = create_categorical_bin_series(self.df[col], max_categories=self.cat_value_limit)
            else:
                binned_values = create_categorical_series_no_missing(self.df[col])
        return binned_values

    def get_control_total_summaries(self):
        control_df_list = []
        for var in self.control_var_list:
            binned_values = self.get_binned_series(var)
            control_var_df = pd.concat([self.df, binned_values], axis=1).groupby(binned_values.name) \
                .apply(self.agg_fcn)
            control_df_list.append(control_var_df)
        return control_df_list

    def get_control_binned_series_dict(self):
        control_bin_series_dict = {}
        for sec_col in self.control_var_list:
            control_bin_series_dict[sec_col] = self.get_binned_series(sec_col)
        return control_bin_series_dict

    def get_var_info_dict(self):
        col_info = {}
        for col in self.df.columns.tolist():
            this_var_info = {}
            binned_values = self.get_binned_series(col)
            # one-way exhibits
            this_var_info['one_way'] = sort_df_by_interval_idx(
                pd.concat([self.df, binned_values], axis=1).groupby(binned_values.name)
                .apply(self.agg_fcn)
            )

            # two way exposure comparisons
            for key, sec_values in self.control_binned_series_dict.items():
                if key != col:
                    # get two way counts
                    two_way_df = pd.concat([binned_values, sec_values], axis=1).groupby(
                            [binned_values.name, sec_values.name]).size().unstack().fillna(0)

                    #  calculate Cramers V... before converting to percentages
                    this_var_info[f'cramers_v_{key}'] = calculate_cramers_v_value(two_way_df)

                    # convert to pct within columns
                    for a_col in two_way_df.columns:
                        col_sum = two_way_df[a_col].sum()
                        two_way_df[a_col] = two_way_df[a_col] / col_sum

                    this_var_info[f'two_way_{key}'] = sort_df_by_interval_idx(two_way_df.copy())

                    # two-way distributions
                    this_var_info[f'bivariate_stats_{key}'] = pd.concat([self.df, binned_values, sec_values], axis=1)\
                        .groupby([sec_values.name, binned_values.name]).apply(self.agg_fcn)

            col_info[col] = this_var_info

        return col_info

    def _calculate_signal(self, one_way_df, metric_col, weight_col):
        book_totals = self.agg_fcn(self.df)
        weight_sse = (one_way_df[weight_col] * ((one_way_df[metric_col] - book_totals[metric_col]) ** 2)).sum()
        signal = ((weight_sse / book_totals[weight_col]) ** 0.5) / book_totals[metric_col]
        return signal

    def _get_series_for_signal_metric(self, metric_col, weight_col):
        signal_metric_dict = {}
        for col in self.df.columns.tolist():
            print(f"_get_series_for_signal_metric for col: {col}")
            col_one_way_df = self.var_info_dict[col]['one_way']
            signal_metric_dict[col] = self._calculate_signal(col_one_way_df, metric_col, weight_col)

        signal_metric_series = pd.Series(signal_metric_dict)
        signal_metric_series.name = f"signal_{metric_col}"

        return signal_metric_series

    def _get_series_for_cramers_v_vs_secondary_var(self, secondary_var):
        cramers_v_dict = {}
        for col in self.df.columns.tolist():
            try:
                cramers_v_dict[col] = self.var_info_dict[col][f'cramers_v_{secondary_var}']
            except KeyError:
                cramers_v_dict[col] = None

        cramers_v_vs_secondary_var_series = pd.Series(cramers_v_dict)
        cramers_v_vs_secondary_var_series.name = f"cramers_v_{secondary_var}"

        return cramers_v_vs_secondary_var_series

    def get_var_summary(self):
        if self.start_with_user_provided_summary_df:
            summary_df = self.user_provided_summary_df
        else:
            summary_df = self.df.describe(include='all').T

        # signal stuff
        signal_series_list = []
        if self.calculate_signals:
            book_totals = self.agg_fcn(self.df)
            agg_metric_columns = list(book_totals.index)
            if self.signal_weight_col:
                weight_col = self.signal_weight_col
            else:
                weight_col = agg_metric_columns[0]  # if no weight provided, assume first column
            for metric_col in [m_col for m_col in agg_metric_columns if m_col != weight_col]:
                signal_metric_series = self._get_series_for_signal_metric(metric_col, weight_col)
                signal_series_list.append(signal_metric_series)

        # cramers V stuff
        cramers_v_series_list = []
        if self.calculate_cramers_v:
            for control_var in self.control_var_list:
                cramers_v_series = self._get_series_for_cramers_v_vs_secondary_var(control_var)
                cramers_v_series_list.append(cramers_v_series)

        summary_df = pd.concat([summary_df] + signal_series_list + cramers_v_series_list, axis=1)
        return summary_df
