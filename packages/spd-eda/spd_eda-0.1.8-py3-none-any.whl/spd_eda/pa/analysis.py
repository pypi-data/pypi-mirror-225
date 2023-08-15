from .config import DB_SERVER, PLOTS_DIR_PATH
from .connection import Connection
from .datasource import DataSource
from .dataview import DataView
from .pa_stats import PAStats

import pandas as pd
from xlsxwriter.utility import xl_range_abs, xl_col_to_name
import matplotlib.pyplot as plt
import seaborn as sns
import os


class Analysis:
    def __init__(self, db_name, analysis_id, rf_keyword_list=[]):
        self.conn = Connection(DB_SERVER, db_name).str
        self.db_name = db_name
        self.analysis_id = analysis_id
        self._rf_keyword_list = rf_keyword_list

        # read analysis details table
        self.analysis_details = self.get_analysis_details()

        # data view & stats connection
        self.dv_name = self.analysis_details.iloc[0]['VIEW_ID']
        self.DV = DataView(self.db_name, self.dv_name)
        self.pa_stats_conn = PAStats(self.conn, self.DV.config)
        self._view_definition = self.get_view_definition()
        self.dv_config_df = pd.DataFrame({
            'setting': list(self.DV.config.keys()),
            'values': list(self.DV.config.values())
        })

        # underlying datasource
        self.ds_name = self._view_definition.query("CATEGORY_TYPE == 'rawdatasource'").iloc[0]['CATEGORY_NAME']
        self.DS = DataSource(self.db_name, self.ds_name, self._rf_keyword_list)

        # experiment/model metadata
        self.experiment_name = self.analysis_details.iloc[0]['EXPERIMENT_ID']
        self._experiment_details = self.get_experiment_details()[['ELEMENT', 'VALUE']]
        self.experiment_info = self.get_model_info()
        self.model_form = self._experiment_details.query("ELEMENT == 'Algorithm Type'").iloc[0]['VALUE']

        # model influences... and submodels
        self.model_influence = self.get_model_influence_per_analysis_id(self.analysis_id)
        self.sig_var_list = self.model_influence['data_element'].tolist()
        self.submodels_info_df = self.identify_submodels()
        self._submodel_influence_dict = self._get_sub_model_influences()
        self.denorm_model_influence = self.get_denormed_model_influence()

        # from the old DEV_Analysis_Components file
        self._stats = self._get_analysis_stats()
        self._score_band_list = self._get_score_band_list()

        # model stability results. Tricky thing is getting training/validation criteria
        self.scoring_results_ALL = self.get_stats_by_scoreband(grouping_var='SCORE', addl_condition='1=1')
        self.scoring_results_TRN = self.get_stats_by_scoreband(grouping_var='SCORE',
                                                               addl_condition=self.experiment_info['TRN_DEFN'])
        self.scoring_results_VAL = self.get_stats_by_scoreband(grouping_var='SCORE',
                                                               addl_condition=self.experiment_info['VAL_DEFN'])

        self.score_distn_over_time = self.get_score_distn_by_time()

        # specific attributes to summarize the analysis... initialize with group_id.
        self.rf_list = []  # initialize... user will update later
        self.custom_attributes = {
            'time_handling': {'name': 'group_id', 'ord_cat': 'cat', 'bin_strategy': 'raw', 'bin_parameter': None}
        }
        self.var_handling_dict = {}

        # feature summaries... initialize as empty until user input is provided.
        self.ftr_info = {}
        self.rf_summary_df = pd.DataFrame([])

    def get_analysis_details(self):
        return pd.read_sql(f"select * from analysis_details where analysis_id = '{self.analysis_id}'", self.conn)

    def get_view_definition(self):
        return pd.read_sql(f"select * from view_definition where view_id = '{self.dv_name}'", self.conn)

    def get_experiment_details(self):
        return pd.read_sql(f"select * from experiment_details where experiment_id = '{self.experiment_name}'",
                           self.conn)

    def find_cols_with_certain_keywords(self, kw_list):
        matching_cols = []
        for col in self.DS.ds_column_list:
            for kw in kw_list:
                if kw.lower() in col.lower() and col not in matching_cols:
                    matching_cols.append(col)
        return matching_cols

    def get_model_info(self):
        info = {'type': self._experiment_details.query("ELEMENT == 'Algorithm Type'").iloc[0]['VALUE']}
        if info['type'] == 'Individual GLM':
            info['objective'] = self._experiment_details.query("ELEMENT == 'GLM Type'").iloc[0]['VALUE']
            info['trn_filter'] = self._experiment_details.query("ELEMENT == 'Data Filter Training'").iloc[0]['VALUE']
            info['val_filter'] = self._experiment_details.query("ELEMENT == 'Data Filter Validation'").iloc[0]['VALUE']
            info['trn_portion'] = self._experiment_details.query("ELEMENT == 'Training Data Portion'").iloc[0]['VALUE']
            info['trn_val_type'] = self._experiment_details.query("ELEMENT == 'UI Sampling Measure'").iloc[0]['VALUE']

        if info['type'] == 'Boosting':
            info['objective'] = self._experiment_details.query("ELEMENT == 'Score Function'").iloc[0]['VALUE']
            info['band_pctages'] = self._experiment_details.query("ELEMENT == 'Score Segmentation Percentage'").iloc[0][
                'VALUE']
            info['trn_portion'] = self._experiment_details.query("ELEMENT == 'Training Data Portion'").iloc[0]['VALUE']
            info['trn_filter'] = self._experiment_details.query("ELEMENT == 'Data Filter Training'").iloc[0]['VALUE']
            info['val_filter'] = self._experiment_details.query("ELEMENT == 'Data Filter Validation'").iloc[0]['VALUE']

        # add my own training and validation filters
        if info.get('trn_portion'):
            thresh = info['trn_portion']
            info['TRN_DEFN'] = f"sysrandnum <= {thresh}"
            info['VAL_DEFN'] = f"sysrandnum > {thresh}"
        else:
            info['TRN_DEFN'] = info['trn_filter']
            info['VAL_DEFN'] = info['val_filter']
        return info

    def get_model_influence_per_analysis_id(self, analysis_id):
        SQL = f"""
            ;with tmp as (
            select subindex, rule_id, group_id
            from rules_data
            where net_id = '{analysis_id}'
            group by subindex, rule_id, group_id
            )
            select
            	GROUP_ID as 'data_element',
            	model_influence = CAST(count(1) as float) /  (select count(1) from tmp)
            from tmp
            group by GROUP_ID
            order by model_influence desc
            """
        return pd.read_sql(SQL, self.conn)

    # submodels
    def identify_submodels(self):
        submodel_list = []
        for tree in self.DS.ds_inheritance_list:
            for column in tree[1]:
                if column[0] in self.sig_var_list:
                    submodel_list.append([column[0], column[2], column[3], column[4]])
        return pd.DataFrame(submodel_list, columns=['var', 'analysis_id', 'analysis_type', 'objective'])

    def _get_sub_model_influences(self):
        sub_inf_dict = {}
        for idx, row in self.submodels_info_df[['var', 'analysis_id']].iterrows():
            sub_inf_dict[row['var']] = self.get_model_influence_per_analysis_id(row['analysis_id'])
        return sub_inf_dict

    def get_denormed_model_influence(self):
        prim_inf_no_subs_df = self.model_influence[
            ~self.model_influence['data_element'].isin(self._submodel_influence_dict.keys())]
        adj_sub_df_list = []
        for rf, inf_df in self._submodel_influence_dict.items():
            prim_inf_pct = self.model_influence.query(f"data_element == '{rf}'").iloc[0]['model_influence']
            df_adj = inf_df.copy()
            df_adj['model_influence'] = df_adj['model_influence'] * prim_inf_pct
            adj_sub_df_list.append(df_adj)

        combined_inf_df = pd.concat([prim_inf_no_subs_df] + adj_sub_df_list).sort_values('model_influence',
                                                                                         ascending=False)
        return combined_inf_df.reset_index(drop=True)

    def _get_analysis_stats(self):
        SQL = f"""
                    select ITERATION_NUM, ATTRIBUTE, VALUE
                    from analysis_summary
                    where analysis_id= '{self.analysis_id}'
                    """
        return pd.read_sql(SQL, self.conn)

    def _get_score_band_list(self):

        SQL = f"select boundary_start from score_boundaries where analysis_id = '{self.analysis_id}' order by boundary_start asc"
        score_band_df = pd.read_sql(SQL, self.conn)

        SQL_pmml_hailmary = f"""
            select a.analysis_id, a.EXPERIMENT_ID,
            	ExperimentType = max(case when b.Element = 'Experiment type' then b.VALUE end),
            	ScoreSegPct = max(case when b.Element = 'Score Segmentation Percentage' then b.VALUE end)
            from analysis_details a
            inner join EXPERIMENT_DETAILS b on a.EXPERIMENT_ID = b.EXPERIMENT_ID and b.ELEMENT in ('Experiment type', 'Score Segmentation Percentage')
            where a.analysis_id = '{self.analysis_id}'
            group by a.analysis_id, a.EXPERIMENT_ID
            """
        score_band_pmml = pd.read_sql(SQL_pmml_hailmary, self.conn)

        if len(score_band_df) > 0:
            score_bucket_list = score_band_df['boundary_start'].tolist()
        elif len(score_band_pmml) == 1:
            if score_band_pmml.iloc[0]['ExperimentType'] == 'PMML':
                pcts = score_band_pmml.iloc[0]['ScoreSegPct']
                score_bucket_list = [int(float(p) * 1000) for p in pcts.split(",")]
            else:
                score_bucket_list = [1, 101, 201, 301, 401, 501, 600, 700, 800, 900]  # ugh, GLMs should fall int othis.
        else:
            score_bucket_list = [1, 200, 500, 800]

        return score_bucket_list

    def get_stats_by_scoreband(self, grouping_var='SCORE', addl_condition='1=1'):
        pa_stats = PAStats(self.conn, self.DV.config)
        df = pa_stats.get_agg_totals(grouping_vars=grouping_var, analysis_id=self.analysis_id,
                                     addl_condition=addl_condition)
        df = pa_stats.apply_fixed_ordinal_bins(df, grouping_var, self._score_band_list)
        return pa_stats._add_relativities(
            pa_stats._add_objectives(
                df.groupby(grouping_var).sum().reset_index()
            ),
        )

    def get_score_distn_by_time(self):
        pa_stats = PAStats(self.conn, self.DV.config)
        df = pa_stats.get_agg_totals(grouping_vars='SCORE, GROUP_ID', analysis_id=self.analysis_id)
        df = pa_stats.apply_fixed_ordinal_bins(df, 'SCORE', self._score_band_list)
        df_agg = df.groupby(['SCORE', 'GROUP_ID'])[['EExp']].sum().unstack().fillna(0)
        df_agg.columns = [t[1] for t in df_agg.columns.values]
        for col in df_agg.columns:
            col_sum = df_agg[col].sum()
            df_agg[col] = df_agg[col] / col_sum
        return df_agg.reset_index()

    def get_score_distn_by_geo(self, geo_info_dict):
        pa_stats = PAStats(self.conn, self.DV.config)
        score_info_info = {
            'name': 'SCORE',
            'ord_cat': 'ord',  # ord, cat
            'bin_strategy': 'engine',  # engine (SCORE only), raw, dataview, on thresholds, manual
            'bin_parameter': None,
        }

        # store it for future use (excel)
        df = pa_stats.get_binned_agg_totals([score_info_info, geo_info_dict], self.DV.dv_imported_elements,
                                            self.analysis_id, self._score_band_list)

        # reshape
        df_agg = df.groupby([score_info_info['name'], geo_info_dict['name']])[['EExp']].sum().unstack().fillna(0)
        df_agg.columns = [t[1] for t in df_agg.columns.values]
        for col in df_agg.columns:
            col_sum = df_agg[col].sum()
            df_agg[col] = df_agg[col] / col_sum

        self.score_distn_over_geo = df_agg
        return self.score_distn_over_geo

    ###################################
    ### Setting Geographic stuff.
    ###################################
    def update_geo_info(self, geo_handling_dict):
        # update the geo handling definition... something like state_handling = {'name': 'CoverageState', 'ord_cat': 'cat', 'bin_strategy': 'dataview', 'bin_parameter': None}
        self.custom_attributes['geo_handling'] = geo_handling_dict

        # univariates by state
        self.custom_attributes['eda_state'] = self.pa_stats_conn._add_objectives(
            self.pa_stats_conn.get_binned_agg_totals(
                [geo_handling_dict], self._view_definition, self.analysis_id, score_band_list=[]
            )
        )

        # univariates by state/time
        obj_to_abbr = {
            'loss ratio': 'LR',
            'Loss Ratio': 'LR',
            'claim frequency': 'Freq',
            'loss cost': 'LC',
            'claim severity': 'Sev'
        }
        agg_geo_yr = self.pa_stats_conn._add_objectives(
            self.pa_stats_conn.get_binned_agg_totals(
                [geo_handling_dict, self.custom_attributes['time_handling']],
                self._view_definition,
                self.analysis_id,
                score_band_list=[]
            )
        )
        obj_to_use = obj_to_abbr[self.experiment_info['objective']]
        agg_geo_yr = agg_geo_yr.pivot_table(index=geo_handling_dict['name'],
                                            columns=self.custom_attributes['time_handling']['name'],
                                            values=['EExp', obj_to_use])
        agg_geo_yr.columns = [f"{c[0]}_{c[1]}" for c in agg_geo_yr.columns]
        self.custom_attributes['eda_state_yr'] = agg_geo_yr.reset_index()

        # score distribution by state
        self.custom_attributes['scores_state'] = self.get_score_distn_by_geo(geo_handling_dict).reset_index()

    # by naics
    def update_naics_info(self, naics_handling_dict):
        # update the geo handling definition... something like state_handling = {'name': 'CoverageState', 'ord_cat': 'cat', 'bin_strategy': 'dataview', 'bin_parameter': None}
        self.custom_attributes['naics_handling'] = naics_handling_dict

        # univariates by state
        self.custom_attributes['eda_naics'] = self.pa_stats_conn._add_objectives(
            self.pa_stats_conn.get_binned_agg_totals(
                [naics_handling_dict], self._view_definition, self.analysis_id, score_band_list=[]
            )
        )

        # score distribution by state
        self.custom_attributes['scores_naics'] = self.get_score_distn_by_geo(naics_handling_dict).reset_index()

    ###################################
    ### For individual variables
    ###################################

    def _update_var_handling_dict(self, rf_list):
        self.rf_list = rf_list
        # just grab binning from data view
        for col in self.rf_list:
            dv_type = self._view_definition.query(
                f"CATEGORY_TYPE in ('ordinal','categorical','compound') and CATEGORY_NAME == '{col}'").iloc[0][
                'CATEGORY_TYPE']
            if dv_type == 'ordinal':
                self.var_handling_dict[col] = {'name': col, 'ord_cat': 'ord', 'bin_strategy': 'dataview',
                                               'bin_parameter': None}
            else:
                self.var_handling_dict[col] = {'name': col, 'ord_cat': 'cat', 'bin_strategy': 'dataview',
                                               'bin_parameter': None}

    def _calculate_ftr_info(self):
        for ftr in self.var_handling_dict.keys():
            this_ftr_info = {}
            this_ftr_info['name'] = ftr
            if ftr in self.DS.ds_all_column_list:
                this_ftr_info['univariate'] = self.pa_stats_conn.one_way_stats(self.var_handling_dict[ftr],
                                                                               self._view_definition, self.analysis_id,
                                                                               score_band_list=[])
                this_ftr_info['exp_distn_by_year'] = self.pa_stats_conn.two_way_value_checks(
                    self.var_handling_dict[ftr], self.custom_attributes['time_handling'], self._view_definition,
                    self.analysis_id, 'EExp', normalize_in_cols=True)
                this_ftr_info['exp_distn_by_geo'] = self.pa_stats_conn.two_way_value_checks(self.var_handling_dict[ftr],
                                                                                            self.custom_attributes[
                                                                                                'geo_handling'],
                                                                                            self._view_definition,
                                                                                            self.analysis_id, 'EExp',
                                                                                            normalize_in_cols=True)
                this_ftr_info['exp_distn_by_naics'] = self.pa_stats_conn.two_way_value_checks(
                    self.var_handling_dict[ftr], self.custom_attributes['naics_handling'], self._view_definition,
                    self.analysis_id, 'EExp', normalize_in_cols=True)
                # signals blowing up with ratios... let it skip
                try:
                    this_ftr_info['w_signals'] = self.pa_stats_conn.get_signals(this_ftr_info['univariate'])
                except:
                    this_ftr_info['w_signals'] = {}
                # 1/27/2022: correlation
                try:
                    this_ftr_info['w_corr'] = self.pa_stats_conn.get_correlations(this_ftr_info['univariate'], ftr)
                except:
                    this_ftr_info['w_corr'] = {}
            else:
                this_ftr_info['univariate'] = pd.DataFrame([])
                this_ftr_info['exp_distn_by_year'] = pd.DataFrame([])
                this_ftr_info['exp_distn_by_geo'] = pd.DataFrame([])
                this_ftr_info['exp_distn_by_naics'] = pd.DataFrame([])
                this_ftr_info['w_signals'] = {}
                # 1/27/2022: correlation
                this_ftr_info['w_corr'] = {}

            self.ftr_info[ftr] = this_ftr_info

    # def _get_internal_nam_for_feature(self, name):
    #     if name in MAPPING_DICT.keys():
    #         return MAPPING_DICT[name]
    #     else:
    #         return ''

    # def _get_risk_factor_metadata_df(self):
    #     rf_meta_df = pd.read_csv(RF_META_FILE_LOCATION, encoding="ISO-8859-1")
    #     rf_meta_df.columns = [col.lower().replace(' ', '_') for col in rf_meta_df.columns.tolist()]
    #     rf_meta_df.rename(
    #         columns={'source': 'datasource', 'directionality_(higher_rf_value_means...)': 'directionality'},
    #         inplace=True)
    #     return rf_meta_df

    def _create_ftr_summary_df(self):
        # 1/27/2022: correlation
        tmp_df = pd.DataFrame(self.ftr_info).T[['name', 'w_signals', 'w_corr']].copy()

        signals_df = tmp_df['w_signals'].apply(pd.Series)
        signals_df.columns = [f"w_signals_{col}" for col in signals_df.columns]
        # 1/27/2022: correlation
        corr_df = tmp_df['w_corr'].apply(pd.Series)
        corr_df.columns = [f"w_corr_{col}" for col in corr_df.columns]
        # 1/27/2022: correlation
        rf_df = pd.concat([tmp_df[['name']], signals_df, corr_df], axis=1).reset_index(drop=True).sort_values('name')

        # add main model
        rf_df = rf_df.merge(
            self.model_influence.rename(columns={'data_element': 'name', 'model_influence': 'inf_final'}), how='left',
            on='name')

        # add sub-models, if they exist
        for sub, inf in self._submodel_influence_dict.items():
            rf_df = rf_df.merge(inf.rename(columns={'data_element': 'name', 'model_influence': f'inf_{sub}'}),
                                how='left', on='name')

            # if I had submodels... add the decomposed influence
        if self._submodel_influence_dict.keys():
            rf_df = rf_df.merge(
                self.denorm_model_influence.rename(columns={'data_element': 'name', 'model_influence': f'inf_AGG'}),
                how='left', on='name')

        # # try to map the names
        # rf_df['internal_name'] = rf_df['name'].apply(lambda x: self._get_internal_nam_for_feature(x))
        # internal_meta = self._get_risk_factor_metadata_df()
        # rf_df = rf_df.merge(internal_meta, how='left', on='internal_name')

        # TODO... how to manage the names
        self.rf_summary_df = rf_df

    def _generate_plots(self, obj='Freq'):
        if not os.path.exists(PLOTS_DIR_PATH):
            os.makedirs(PLOTS_DIR_PATH)
        for ftr in self.ftr_info.keys():
            ftr_nm = self.ftr_info[ftr]['name']
            try:
                plt.ioff()
                fig, axs = plt.subplots(figsize=(9, 4))
                df = self.ftr_info[ftr]['univariate']
                sns.barplot(data=df, x=ftr_nm, y='EExp', color='steelblue', alpha=0.5, ax=axs)
                axs2 = axs.twinx()
                sns.pointplot(data=df, x=ftr_nm, y=obj, color='black', ax=axs2)
                plt.savefig(f"{PLOTS_DIR_PATH}/{self.db_name}_{self.analysis_id}_{ftr_nm}_{obj}.png")
                plt.clf()
            except:
                pass

    def process_features(self, rf_list, obj_fcn='Freq', include_charts=True):
        self._update_var_handling_dict(rf_list)
        self._calculate_ftr_info()
        self._create_ftr_summary_df()
        if include_charts:
            self._generate_plots(obj=obj_fcn)

    ###################################
    ### Writing content
    ###################################
    def _format_it(self, workbook, worksheet, df, df_startrow, df_startcol, obj_to_format, col_format_dict,
                   gradient_entire_range=False):

        my_white = '#ffffff'
        my_red = '#ff0000'

        first_row = df_startrow
        first_col = df_startcol
        last_row = df_startrow + df.shape[0]
        last_col = df_startcol + df.shape[1]

        # for objective functions
        for obj in obj_to_format:
            if obj in df.columns.tolist():
                obj_col_idx = df.columns.tolist().index(obj)
                col_nbr = df_startcol + obj_col_idx
                cell_range = xl_range_abs(first_row, col_nbr, last_row, col_nbr)
                worksheet.conditional_format(cell_range,
                                             {'type': '2_color_scale', 'min_color': my_white, 'max_color': my_red})

        for col, format_string in col_format_dict.items():
            the_format = workbook.add_format({'num_format': format_string})
            if col in df.columns.tolist():
                col_idx = df.columns.tolist().index(col)
                col_nbr = df_startcol + col_idx
                col_letter = xl_col_to_name(col_nbr)
                worksheet.set_column(f'{col_letter}:{col_letter}', 15, the_format)

        # for entire range
        if gradient_entire_range:
            # ignore the first column
            cell_range = xl_range_abs(first_row, first_col + 1, last_row, last_col)
            worksheet.conditional_format(cell_range,
                                         {'type': '2_color_scale', 'min_color': my_white, 'max_color': my_red})

        # zoom it
        worksheet.set_zoom(80)

    def export_summary(self, filename, obj_to_format, stats_formatting):
        # formatting defaults
        DEFAULT_START_ROW = 2
        DEFAULT_START_COL = 1

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        workbook = writer.book

        # config
        self.dv_config_df.to_excel(writer, sheet_name="dv_config", startrow=DEFAULT_START_ROW,
                                   startcol=DEFAULT_START_COL, index=False)

        # by year
        self.DV.control_totals.to_excel(writer, sheet_name="eda_by_year", startrow=DEFAULT_START_ROW,
                                        startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["eda_by_year"]
        self._format_it(workbook, worksheet,
                        df=self.DV.control_totals, df_startrow=DEFAULT_START_ROW, df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # by state
        self.custom_attributes['eda_state'].to_excel(writer, sheet_name="eda_by_state", startrow=DEFAULT_START_ROW,
                                                     startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["eda_by_state"]
        self._format_it(workbook, worksheet,
                        df=self.custom_attributes['eda_state'], df_startrow=DEFAULT_START_ROW,
                        df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # by naics
        self.custom_attributes['eda_naics'].to_excel(writer, sheet_name="eda_by_naics", startrow=DEFAULT_START_ROW,
                                                     startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["eda_by_naics"]
        self._format_it(workbook, worksheet,
                        df=self.custom_attributes['eda_naics'], df_startrow=DEFAULT_START_ROW,
                        df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # by state
        self.custom_attributes['eda_state_yr'].to_excel(writer, sheet_name="eda_state_yr", startrow=DEFAULT_START_ROW,
                                                        startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["eda_state_yr"]
        self._format_it(workbook, worksheet,
                        df=self.custom_attributes['eda_state_yr'], df_startrow=DEFAULT_START_ROW,
                        df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # analysis info
        pd.DataFrame(self.experiment_info, index=['parameter']).to_excel(writer, sheet_name="model_params",
                                                                         startrow=DEFAULT_START_ROW,
                                                                         startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["model_params"]
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # model stability
        self.scoring_results_TRN.to_excel(writer, sheet_name="model_stability", startrow=DEFAULT_START_ROW,
                                          startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["model_stability"]
        worksheet.write(DEFAULT_START_ROW - 1, DEFAULT_START_COL - 1, 'TRAINING data')
        self._format_it(workbook, worksheet,
                        df=self.scoring_results_TRN, df_startrow=DEFAULT_START_ROW, df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        new_start_row = DEFAULT_START_ROW + self.scoring_results_TRN.shape[0] + 5
        self.scoring_results_VAL.to_excel(writer, sheet_name="model_stability", startrow=new_start_row,
                                          startcol=DEFAULT_START_COL, index=False)
        worksheet.write(new_start_row - 1, DEFAULT_START_COL - 1, 'VALIDATION data')
        self._format_it(workbook, worksheet,
                        df=self.scoring_results_VAL, df_startrow=new_start_row, df_startcol=DEFAULT_START_COL,
                        obj_to_format=obj_to_format,
                        col_format_dict=stats_formatting
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # score distn over time &  geo
        self.score_distn_over_time.to_excel(writer, sheet_name="scores_by_year_geo", startrow=DEFAULT_START_ROW,
                                            startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["scores_by_year_geo"]
        self._format_it(workbook, worksheet,
                        df=self.score_distn_over_time, df_startrow=DEFAULT_START_ROW, df_startcol=DEFAULT_START_COL,
                        obj_to_format=[],
                        col_format_dict={col: '0.00%' for col in self.score_distn_over_time.columns},
                        gradient_entire_range=True
                        )
        new_start_row = DEFAULT_START_ROW + self.score_distn_over_time.shape[0] + 5
        self.custom_attributes['scores_state'].to_excel(writer, sheet_name="scores_by_year_geo", startrow=new_start_row,
                                                        startcol=DEFAULT_START_COL, index=False)
        self._format_it(workbook, worksheet,
                        df=self.custom_attributes['scores_state'], df_startrow=new_start_row,
                        df_startcol=DEFAULT_START_COL,
                        obj_to_format=[],
                        col_format_dict={col: '0.00%' for col in self.score_distn_over_time.columns},
                        gradient_entire_range=True
                        )
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # model influence: self.model_influence
        self.model_influence.to_excel(writer, sheet_name="influence", startrow=DEFAULT_START_ROW,
                                      startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["influence"]
        self._format_it(workbook, worksheet,
                        df=self.model_influence, df_startrow=DEFAULT_START_ROW, df_startcol=DEFAULT_START_COL,
                        obj_to_format=['model_influence'],
                        col_format_dict={'model_influence': '0.00%'}
                        )
        for idx, rf in enumerate(self.model_influence['data_element'].tolist()):
            try:
                var_sheet_idx = self.rf_summary_df['name'].tolist().index(rf)
                linked_sheet = f"rf_{str(var_sheet_idx)}"
                worksheet.write_url(DEFAULT_START_ROW + 1 + idx, DEFAULT_START_COL, f'internal: {linked_sheet}!A1',
                                    string=rf)
            except ValueError:
                pass

        new_start_col = DEFAULT_START_COL + self.model_influence.shape[1] + 1
        for idx, row in self.submodels_info_df.iterrows():
            worksheet.write(DEFAULT_START_ROW, new_start_col,
                            f"{row['var']} ({row['objective']}_{row['analysis_type']}_{row['analysis_id']})")
            self._submodel_influence_dict[row['var']].to_excel(writer, sheet_name="influence",
                                                               startrow=DEFAULT_START_ROW + 1, startcol=new_start_col,
                                                               index=False)
            self._format_it(workbook, worksheet,
                            df=self._submodel_influence_dict[row['var']], df_startrow=DEFAULT_START_ROW + 1,
                            df_startcol=new_start_col,
                            obj_to_format=['model_influence'],
                            col_format_dict={'model_influence': '0.00%'}
                            )
            for idx, rf in enumerate(self._submodel_influence_dict[row['var']]['data_element'].tolist()):
                try:
                    var_sheet_idx = self.rf_summary_df['name'].tolist().index(rf)
                    linked_sheet = f"rf_{str(var_sheet_idx)}"
                    worksheet.write_url(DEFAULT_START_ROW + 2 + idx, new_start_col, f'internal: {linked_sheet}!A1',
                                        string=rf)
                except ValueError:
                    pass
            new_start_col = new_start_col + 3

        worksheet.write(DEFAULT_START_ROW, new_start_col, f"Decomposed Influences")
        self.denorm_model_influence.to_excel(writer, sheet_name="influence", startrow=DEFAULT_START_ROW + 1,
                                             startcol=new_start_col, index=False)
        self._format_it(workbook, worksheet,
                        df=self.denorm_model_influence, df_startrow=DEFAULT_START_ROW + 1, df_startcol=new_start_col,
                        obj_to_format=['model_influence'],
                        col_format_dict={'model_influence': '0.00%'}
                        )
        for idx, rf in enumerate(self.denorm_model_influence['data_element'].tolist()):
            try:
                var_sheet_idx = self.rf_summary_df['name'].tolist().index(rf)
                linked_sheet = f"rf_{str(var_sheet_idx)}"
                worksheet.write_url(DEFAULT_START_ROW + 2 + idx, new_start_col, f'internal: {linked_sheet}!A1',
                                    string=rf)
            except ValueError:
                pass
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # main variable tab
        # TODO -- which objective to consistently highlight!!!!!
        self.rf_summary_df.to_excel(writer, sheet_name="variables", startrow=DEFAULT_START_ROW,
                                    startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["variables"]

        format_dict = {}
        for col in [col for col in self.rf_summary_df.columns.tolist() if 'w_signals' in col]:
            format_dict[col] = '0.00'
        for col in [col for col in self.rf_summary_df.columns.tolist() if 'inf_' in col]:
            format_dict[col] = '0.00%'

        self._format_it(workbook, worksheet,
                        df=self.rf_summary_df, df_startrow=DEFAULT_START_ROW, df_startcol=DEFAULT_START_COL,
                        obj_to_format=[col for col in self.rf_summary_df.columns.tolist() if obj_to_format[0] in col],
                        col_format_dict=format_dict
                        )
        for idx, rf in enumerate(self.rf_summary_df['name'].tolist()):  # ugly, but keeps links aligned with content
            this_sheet = f"rf_{str(idx)}"
            worksheet.write_url(DEFAULT_START_ROW + 1 + idx, DEFAULT_START_COL, f'internal: {this_sheet}!A1', string=rf)

        # individidual risk factor exhibits
        CHART_ROW_PADDING = 20
        indiv_start_row = DEFAULT_START_ROW + CHART_ROW_PADDING
        for idx, rf in enumerate(self.rf_summary_df['name'].tolist()):  # ugly, but keeps links aligned with content
            this_sheet = f"rf_{str(idx)}"

            # univariate stats
            uni_df = self.ftr_info[rf]['univariate']
            uni_df.to_excel(writer, sheet_name=this_sheet, startrow=indiv_start_row, startcol=DEFAULT_START_COL,
                            index=False)
            worksheet = writer.sheets[this_sheet]
            self._format_it(workbook, worksheet,
                            df=uni_df, df_startrow=indiv_start_row, df_startcol=DEFAULT_START_COL,
                            obj_to_format=obj_to_format,
                            col_format_dict=stats_formatting
                            )
            # exposure over time
            new_start_col = DEFAULT_START_COL + uni_df.shape[1] + 1
            time_df = self.ftr_info[rf]['exp_distn_by_year']
            time_df.to_excel(writer, sheet_name=this_sheet, startrow=indiv_start_row, startcol=new_start_col,
                             index=False)
            worksheet = writer.sheets[this_sheet]
            self._format_it(workbook, worksheet,
                            df=time_df, df_startrow=indiv_start_row, df_startcol=new_start_col,
                            obj_to_format=obj_to_format,
                            col_format_dict={col: '0.00%' for col in time_df.columns[1:]},
                            gradient_entire_range=True
                            )

            # exposure by geography
            new_start_row = indiv_start_row + time_df.shape[0] + 5
            geo_df = self.ftr_info[rf]['exp_distn_by_geo']
            geo_df.to_excel(writer, sheet_name=this_sheet, startrow=new_start_row, startcol=new_start_col, index=False)
            worksheet = writer.sheets[this_sheet]
            self._format_it(workbook, worksheet,
                            df=geo_df, df_startrow=new_start_row, df_startcol=new_start_col,
                            obj_to_format=obj_to_format,
                            col_format_dict={col: '0.00%' for col in geo_df.columns[1:]},
                            gradient_entire_range=True
                            )

            # exposure by geography
            new_start_row = new_start_row + geo_df.shape[0] + 5
            naics_df = self.ftr_info[rf]['exp_distn_by_naics']
            naics_df.to_excel(writer, sheet_name=this_sheet, startrow=new_start_row, startcol=new_start_col,
                              index=False)
            worksheet = writer.sheets[this_sheet]
            self._format_it(workbook, worksheet,
                            df=naics_df, df_startrow=new_start_row, df_startcol=new_start_col,
                            obj_to_format=obj_to_format,
                            col_format_dict={col: '0.00%' for col in geo_df.columns[1:]},
                            gradient_entire_range=True
                            )

            worksheet.set_zoom(70)
            worksheet.hide_gridlines(2)
            worksheet.insert_image('C1',
                                   f"{PLOTS_DIR_PATH}/{self.db_name}_{self.analysis_id}_{rf}_{obj_to_format[0]}.png")
            worksheet.write_url('A1', 'internal: variables!A1', string="variables")
            worksheet.write_url('A2', 'internal: influence!A1', string="influence")

        writer.save()
