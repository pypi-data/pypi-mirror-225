import pandas as pd
import numpy as np
import math
import scipy.stats as scs
from .config import MAX_DISTINCT_CAT_VALUES_IF_UNBUCKETED


class PAStats:
    def __init__(self, conn, dv_config):
        self.conn = conn
        self.dv_config = dv_config

    ###############################################
    # Methods for producing stats
    ###############################################

    def _add_relativities(self, df, obj_cols=['Freq', 'Sev', 'LC', 'LR']):
        if df.shape[0] > 0:
            book_avg = self._add_objectives(df[['rec_ct', 'EExp', 'EP', 'CC', 'IL']].sum())
            for obj in obj_cols:
                df[f"{obj}_rel"] = df[obj] / book_avg[obj]
            return df
        else:
            return None

    def _add_objectives(self, df):
        if df.shape[0] > 0:
            df['LR'] = df['IL'] / df['EP']
            df['Freq'] = df['CC'] / df['EExp']
            df['Sev'] = df['IL'] / df['CC']
            df['LC'] = df['IL'] / df['EExp']
            try:
                df['pct_with_claim'] = df['has_claim'] / df['rec_ct']
            except:
                pass
            return df
        else:
            return None

    def _all_cols_but_group_id(self, analysis_id):
        sql = f"""
        select COLUMN_NAME from INFORMATION_SCHEMA.columns where table_name = 'landed_data_scores_{analysis_id}'
        """
        col_list = list(pd.read_sql(sql, self.conn)['COLUMN_NAME'])
        return ", ".join([col for col in col_list if col.upper() != 'GROUP_ID'])

    def get_agg_totals(self, grouping_vars, analysis_id, addl_condition="1=1", all_desc="ALL"):
        # if referencing score, need to join to the scores table
        if "SCORE" in grouping_vars.upper().split(
                ','):  # does this ensure that any variable containing the string "text" doesn't blow up?
            all_cols_by_group_id = self._all_cols_but_group_id(analysis_id)
            score_sql_if_needed = f"""
                        left outer join (
                                        select {all_cols_by_group_id}
                                        from [landed_data_scores_{analysis_id}]
                                        ) b on a.policyno = b.policyno
                        """
        else:
            score_sql_if_needed = ""

        if grouping_vars == '':
            grouping_vars = f"'{all_desc}' as 'sample'"
            disable_grp_by = "--"
            disable_order_by = "--"
        else:
            disable_grp_by = ""
            disable_order_by = ""

        # blank loss caps are a problem... just set them to the loss definition if they're blank
        if self.dv_config['loss_cap'] == '':
            self.dv_config['loss_cap'] = self.dv_config['IL']

        sql_grp = f"""
        select
            {grouping_vars}
            ,rec_ct = sum(case when {self.dv_config['exp_defn']} then 1 end)
            ,EExp = sum(case when {self.dv_config['exp_defn']} then {self.dv_config['EExp']} end)
            ,EP = sum(case when {self.dv_config['exp_defn']} then {self.dv_config['EP']} end)
            ,has_claim = sum(case when {self.dv_config['clm_defn']} then 1 else 0 end)
            ,CC = sum(case when {self.dv_config['clm_defn']} then {self.dv_config['CC']} else 0 end)
            ,IL = sum(case when {self.dv_config['clm_defn']} then
                                                    (case when {self.dv_config['IL']} > {self.dv_config['loss_cap']} then {self.dv_config['loss_cap']} else {self.dv_config['IL']} end)
                                                    end)
        from {self.dv_config['datasource']} a
        {score_sql_if_needed}
        where {self.dv_config['dv_filter']} and {addl_condition}
        {disable_grp_by}group by {grouping_vars}
        {disable_order_by}order by {grouping_vars}
        """
        return pd.read_sql(sql_grp, self.conn)

    ###############################################
    # Ordinal binning methods
    ###############################################

    def apply_fixed_ordinal_bins(self, agg_df, cut_col, left_endpoint_list):
        # edge case: database has varchar type, but only numeric values.  Python interprets as string, so convert them.
        if agg_df[cut_col].dtype == 'object':
            agg_df[cut_col] = agg_df[cut_col].astype(float)

        cutpoints = left_endpoint_list
        # makes sure I cover the values
        if agg_df[cut_col].max() >= cutpoints[-1]:
            cutpoints.append(agg_df[cut_col].max() + 1)

        if agg_df[cut_col].min() < cutpoints[0]:
            cutpoints = [agg_df[cut_col].min()] + cutpoints

        agg_df[cut_col] = pd.cut(agg_df[cut_col], bins=cutpoints, right=False, duplicates='drop', include_lowest=True)
        return agg_df

    def get_ordinal_bin_list_from_dataview(self, cut_col, view_def):
        # grab dv row
        this_row = view_def.query(f"CATEGORY_NAME == '{cut_col}' and CATEGORY_TYPE == 'ordinal'")[
            ['CATEGORY_NAME', 'CATEGORY_TYPE', 'INFO_1', 'INFO_2']]
        if this_row.shape[0] == 1:
            raw_bin_list = [int(bin) for bin in this_row.iloc[0]['INFO_1'].split(',')]
            info2_list = this_row.iloc[0]['INFO_2'].split(';')
            for info_2_item in info2_list:
                if "@MULTIPLIER" in info_2_item:
                    multiplier_amt = float(info_2_item.split("=")[-1])
                    raw_bin_list = [(bin * multiplier_amt) for bin in raw_bin_list]
                    # if initial bin was negative, reset to -1 (i.e. no multiplier applied)
                    if raw_bin_list[0] < 0:
                        raw_bin_list[0] = -1
            return raw_bin_list

    def get_ordinal_bin_list_from_agg_distn(self, agg_df, cut_col, num_bins, agg_metric='EExp'):
        df = agg_df.sort_values(cut_col, ascending=True).copy()
        df['pct_metric'] = df[agg_metric].cumsum() / df[agg_metric].sum()

        # figure out bin spacing... convert to percentile
        bin_width = 1 / num_bins
        pctiles_to_search = [i * bin_width for i in range(num_bins)][1:]
        pctiles_to_search

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

    ###############################################
    # Categorical binning methods
    ###############################################

    def apply_fixed_categorical_bins(self, agg_df, cut_col, stand_alone_value_list, fallback_val='@Other'):
        # if bucketing is blank, treat all values as stand-alone if there are fewer than 30 values
        if len(stand_alone_value_list) == 0 and agg_df[cut_col].nunique() <= MAX_DISTINCT_CAT_VALUES_IF_UNBUCKETED:
            return agg_df
        agg_df.loc[~agg_df[cut_col].isin(stand_alone_value_list), cut_col] = fallback_val
        return agg_df

    def get_categorical_bin_list_from_agg_distn(self, agg_df, cut_col, agg_metric='EExp', agg_metric_pct_thresh=0.03):
        tmp_agg = agg_df.groupby(cut_col)[[agg_metric]].sum().reset_index()
        tmp_agg['pct'] = tmp_agg[[agg_metric]] / tmp_agg[[agg_metric]].sum()
        return tmp_agg.query(f"pct > {agg_metric_pct_thresh}")[cut_col].tolist()

    def get_categorical_bin_list_from_dataview(self, cut_col, view_def):
        # grab dv row
        this_row = view_def.query(f"CATEGORY_NAME == '{cut_col}' and CATEGORY_TYPE == 'categorical'")[
            ['CATEGORY_NAME', 'CATEGORY_TYPE', 'INFO_1', 'INFO_2']]
        if this_row.shape[0] == 1:
            raw_bin_list = [bin for bin in this_row.iloc[0]['INFO_1'].split(',')]
            return [bin for bin in raw_bin_list if bin != '@OTHER']

    ###############################################
    # Utilities for producing binned n-way aggregates
    ###############################################
    def _handle_var_info(self, df, var_info, score_bands, view_definition):
        if var_info['ord_cat'] == 'ord':
            if var_info['bin_strategy'] == 'engine':
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], score_bands)
            elif var_info['bin_strategy'] == 'dataview':
                bin_list = self.get_ordinal_bin_list_from_dataview(var_info['name'], view_definition)
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'process':
                bin_list = self.get_ordinal_bin_list_from_agg_distn(df, var_info['name'], var_info['bin_parameter'],
                                                                    agg_metric='EExp')
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'fixed':
                bin_list = var_info['bin_parameter']
                df = self.apply_fixed_ordinal_bins(df, var_info['name'], bin_list)
        elif var_info['ord_cat'] == 'cat':
            if var_info['bin_strategy'] == 'dataview':
                bin_list = self.get_categorical_bin_list_from_dataview(var_info['name'], view_definition)
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'process':
                bin_list = self.get_categorical_bin_list_from_agg_distn(df, var_info['name'], agg_metric='EExp',
                                                                        agg_metric_pct_thresh=var_info['bin_parameter'])
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
            elif var_info['bin_strategy'] == 'fixed':
                bin_list = var_info['bin_parameter']
                df = self.apply_fixed_categorical_bins(df, var_info['name'], bin_list)
        return df

    def get_binned_agg_totals(self, var_info_list, view_definition, analysis_id, score_band_list):
        # grab raw data
        grp_var_str = [var_info['name'] for var_info in var_info_list]
        df = self.get_agg_totals(grouping_vars=",".join(grp_var_str), analysis_id=analysis_id)

        # bucket as specified
        for var_info in var_info_list:
            df = self._handle_var_info(df, var_info, score_band_list, view_definition)

        return df.groupby(grp_var_str).sum().reset_index()

    def get_two_way_eexp_distn(self, var_info1, var_info2, view_definition, analysis_id):
        # store it for future use (excel)
        df = self.get_binned_agg_totals([var_info1, var_info2], view_definition, analysis_id=analysis_id,
                                        score_band_list=[])

        # reshape
        df_agg = df.groupby([var_info1['name'], var_info2['name']])[['EExp']].sum().unstack().fillna(0)
        df_agg.columns = [t[1] for t in df_agg.columns.values]
        for col in df_agg.columns:
            col_sum = df_agg[col].sum()
            df_agg[col] = df_agg[col] / col_sum

        return df_agg

    ###############################################
    # Convenience wrappers on the utility fcns for insurance stats
    ###############################################

    def one_way_stats(self, var_info, view_definition, analysis_id, score_band_list=[]):
        return self._add_relativities(
            self._add_objectives(
                self.get_binned_agg_totals([var_info], view_definition, analysis_id, score_band_list)
            )
        )

    def two_way_value_checks(self, v1_info, v2_info, view_definition, analysis_id, metric_of_interest='EExp',
                             normalize_in_cols=True):
        # edge case when v1 and v2 are the same variables... kills the SQL query, so I'll query with one instance & manually duplicate
        if v1_info['name'] != v2_info['name']:
            agg_df = self._add_objectives(
                self.get_binned_agg_totals([v1_info, v2_info], view_definition, analysis_id, score_band_list=[]))
            agg_df = agg_df.groupby([v1_info['name'], v2_info['name']])[[metric_of_interest]].sum().unstack()
            agg_df.columns = [t[1] for t in agg_df.columns.values]
        else:
            # only use one instance... manually copy the column & then group.unstack
            agg_df = self._add_objectives(
                self.get_binned_agg_totals([v1_info], view_definition, analysis_id, score_band_list=[]))
            agg_df[f"{v1_info['name']}_copy"] = agg_df[v1_info['name']]
            agg_df = agg_df.groupby([v1_info['name'], f"{v1_info['name']}_copy"])[[metric_of_interest]].sum().unstack()
            agg_df.columns = [t[1] for t in agg_df.columns.values]

        if normalize_in_cols:
            for col in agg_df.columns:
                col_sum = agg_df[col].sum()
                agg_df[col] = agg_df[col] / col_sum
        return agg_df.reset_index()

    ###############################################
    # Signal calculations
    ###############################################
    def _calculate_signal(self, df, metric_col):
        # restate totals... since incoming df may have already been filtered
        totals = self._add_objectives(df[['EExp', 'EP', 'CC', 'IL', 'has_claim']].sum())
        book_metric = totals[metric_col]
        book_exposure = totals['EExp']

        # calculate signal... copy df to not indavertently edit inplace
        df2 = df.copy()
        df2['wgt_SSE'] = df2.apply(lambda x: x.EExp * (x[metric_col] - book_metric) * (x[metric_col] - book_metric),
                                   axis=1)
        signal = math.pow(df2['wgt_SSE'].sum() / book_exposure, 0.5) / book_metric
        return signal

    def get_signals(self, univariate_stats, objective_list=['Freq', 'Sev', 'LC', 'LR']):
        signals = {}
        for objective in objective_list:
            signals[objective] = self._calculate_signal(univariate_stats, objective)
        return signals

    ###############################################
    # Correlation calculations
    ###############################################
    def _m(self, x, w):
        """Weighted Mean"""
        return np.sum(x * w) / np.sum(w)

    def _cov(self, x, y, w):
        """Weighted Covariance"""
        return np.sum(w * (x - self._m(x, w)) * (y - self._m(y, w))) / np.sum(w)

    def _weighted_corr(self, x, y, w):
        """Weighted Correlation"""
        return self._cov(x, y, w) / np.sqrt(self._cov(x, x, w) * self._cov(y, y, w))

    # TODO: fix correlations... ordinals need to use the INDEX (and assume they're ordered) instead of the category; just blank it for Categoricals.
    def get_correlations(self, univariate_stats, ftr_nm, objective_list=['Freq', 'Sev', 'LC', 'LR']):
        correlations = {}
        for objective in objective_list:
            correlations[objective] = self._weighted_corr(x=univariate_stats[ftr_nm], y=univariate_stats[objective],
                                                          w=univariate_stats['EExp'])
        return correlations

    ###############################################
    ### Cramers V calculations
    ###############################################
    def _calculate_cramers_v_value(self, contingency_table):
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

    def calculate_cramers_v(self, v1_info, v2_info, view_definition, weight_col='EExp'):
        agg_df = self.get_binned_agg_totals([v1_info, v2_info], view_definition, analysis_id='', score_band_list=[])
        sums_df = agg_df.groupby([v1_info['name'], v2_info['name']])[weight_col].sum().unstack().fillna(0)
        return self._calculate_cramers_v_value(sums_df)

    def get_cramers_v_values(self, ftr_name, secondary_var_list, var_handling_dict, view_definition):
        cramers_v_dict = {}
        for sec_var in secondary_var_list:
            try:
                cv_val = self.calculate_cramers_v(
                    var_handling_dict[ftr_name],
                    var_handling_dict[sec_var],
                    view_definition,
                    weight_col='EExp')
            except:
                cv_val = None
            cramers_v_dict[sec_var] = cv_val
        return cramers_v_dict

