from .config import DB_SERVER, INS_STATS_FORMATTING_DICT, PLOTS_DIR_PATH
from .connection import Connection
from .dataview import DataView
from .pa_stats import PAStats

import pandas as pd
from xlsxwriter.utility import xl_range_abs, xl_col_to_name
import matplotlib.pyplot as plt
import seaborn as sns
import os


class DataViewEda:
    def __init__(self, db_name, dv_name, secondary_var_list=[], bin_override_dict={}):
        self.db_name = db_name
        self.conn = Connection(DB_SERVER, db_name).str
        self.secondary_var_list = secondary_var_list
        self.bin_override_dict = bin_override_dict

        self.dv_name = dv_name

        # data view
        self.DV = DataView(self.db_name, self.dv_name)
        self.dv_config_df = pd.DataFrame({
            'setting': list(self.DV.config.keys()),
            'values': list(self.DV.config.values())
        })
        self._view_definition = self.get_view_definition()

        # data elements and how they're handled
        self.data_element_list = self.DV.dv_imported_elements['CATEGORY_NAME'].tolist()
        self.var_handling_dict = self._update_var_handling_dict()

        # underlying datasource... do I need this?
        self.ds_name = self._view_definition.query("CATEGORY_TYPE == 'rawdatasource'").iloc[0]['CATEGORY_NAME']

        # stats object
        self.pa_stats_conn = PAStats(self.conn, self.DV.config)

        # For each secondary variable, add a control total
        self.secondary_control_totals = {}
        for var in secondary_var_list:
            self.secondary_control_totals[var] = self.pa_stats_conn.one_way_stats(self.var_handling_dict[var],
                                                                                  self._view_definition, '', [])
        # For each secondary variable, two-way distributions of feature within secondary
        # feature summaries... initialize as empty until user input is provided.
        self.ftr_info = {}
        self.ftr_summary_df = pd.DataFrame([])

        # calculate stuff
        self._calculate_ftr_info()
        self._create_ftr_summary_df()

        # plots
        self._generate_plots()

    def get_view_definition(self):
        return pd.read_sql(f"select * from view_definition where view_id = '{self.dv_name}'", self.conn)

    def _update_var_handling_dict(self):
        var_handling_dict = {}
        # just grab binning from data view
        for col in self.data_element_list:
            dv_type = self._view_definition.query(
                f"CATEGORY_TYPE in ('ordinal','categorical','compound') and CATEGORY_NAME == '{col}'").iloc[0][
                'CATEGORY_TYPE']
            if dv_type == 'ordinal':
                var_handling_dict[col] = {'name': col, 'ord_cat': 'ord', 'bin_strategy': 'dataview',
                                          'bin_parameter': None}
            else:
                var_handling_dict[col] = {'name': col, 'ord_cat': 'cat', 'bin_strategy': 'dataview',
                                          'bin_parameter': None}

        for col, handling_dict in self.bin_override_dict.items():
            var_handling_dict[col] = handling_dict

        return var_handling_dict

    def _calculate_ftr_info(self):
        for ftr in self.var_handling_dict.keys():
            this_ftr_info = {}
            this_ftr_info['name'] = ftr
            this_ftr_info['univariate'] = self.pa_stats_conn.one_way_stats(self.var_handling_dict[ftr],
                                                                           self._view_definition, '',
                                                                           score_band_list=[])

            # two-way univariates by secondary variables (where possible... get errors if primary=secondary)
            this_ftr_info['secondary_univariate'] = {}
            for sec_var in self.secondary_var_list:
                try:
                    two_way_stats = self.pa_stats_conn._add_objectives(
                        self.pa_stats_conn.get_binned_agg_totals(
                            [self.var_handling_dict[sec_var], self.var_handling_dict[ftr]],
                            self._view_definition,
                            analysis_id='',
                            score_band_list=[]
                        )
                    )
                    two_way_df = two_way_stats.groupby(self.var_handling_dict[sec_var]['name']).apply(
                        lambda x: self.pa_stats_conn._add_relativities(x)).copy()
                    this_ftr_info['secondary_univariate'][sec_var] = two_way_df
                except:
                    this_ftr_info['secondary_univariate'][sec_var] = pd.DataFrame([])

            # two-way distributions by secondary variables (where possible... get errors if primary=secondary)
            this_ftr_info['exp_distn'] = {}
            for sec_var in self.secondary_var_list:
                try:
                    this_ftr_info['exp_distn'][sec_var] = self.pa_stats_conn.get_two_way_eexp_distn(
                        self.var_handling_dict[ftr], self.var_handling_dict[sec_var], self._view_definition, '')
                except:
                    this_ftr_info['exp_distn'][sec_var] = pd.DataFrame([])
            this_ftr_info['w_signals'] = self.pa_stats_conn.get_signals(this_ftr_info['univariate'])

            # correlations
            try:
                this_ftr_info['w_corr'] = self.pa_stats_conn.get_correlations(this_ftr_info['univariate'], ftr)
            except:
                this_ftr_info['w_corr'] = {}

            # cramers V
            try:
                this_ftr_info['cramers_v'] = self.pa_stats_conn.get_cramers_v_values(ftr, self.secondary_var_list,
                                                                                     self.var_handling_dict,
                                                                                     self._view_definition)
            except:
                this_ftr_info['cramers_v'] = {}

            self.ftr_info[ftr] = this_ftr_info

    def _extract_tabular_info_from_ftr_info(self, cols_to_extract=['name', 'w_signals', 'w_corr', 'cramers_v']):
        all_records = []
        for key_val in self.ftr_info.keys():
            this_record = []
            for col in cols_to_extract:
                this_record.append(self.ftr_info[key_val][col])
            all_records.append(this_record)

        return pd.DataFrame(all_records, columns=cols_to_extract)

    def _create_ftr_summary_df(self, cols_to_extract=['name', 'w_signals', 'w_corr', 'cramers_v']):
        tmp_df = self._extract_tabular_info_from_ftr_info(cols_to_extract)

        signals_df = tmp_df['w_signals'].apply(pd.Series)
        signals_df.columns = [f"w_signals_{col}" for col in signals_df.columns]

        corr_df = tmp_df['w_corr'].apply(pd.Series)
        corr_df.columns = [f"w_corr_{col}" for col in corr_df.columns]

        cv_df = tmp_df['cramers_v'].apply(pd.Series)
        cv_df.columns = [f"cramers_v_{col}" for col in cv_df.columns]

        rf_df = pd.concat([tmp_df[['name']], signals_df, corr_df, cv_df], axis=1).reset_index(drop=True).sort_values(
            'name')

        # add training indicators
        is_trn_idx = rf_df['name'].isin(self.DV.dv_training_list)
        rf_df.loc[is_trn_idx, 'training'] = 'Y'
        rf_df.loc[~is_trn_idx, 'training'] = ''  # blank is easier to see in the output, tbh.

        # beef up the information from dataview
        excluded_types = ['custom claim count field', 'custom expo field', 'custom loss field', 'custom loss mode',
                          'custom premium field', 'custom premium mode', 'filter', 'loss cap amount', 'rawdatasource',
                          'use null as unknown', 'native data types'
                          ]
        addl_info_df = self._view_definition[~self._view_definition['CATEGORY_TYPE'].isin(excluded_types)]
        cols_to_include = ['CATEGORY_NAME', 'CATEGORY_TYPE', 'INFO_1', 'INFO_2', 'VARIATE', 'USED_FOR_TRAINING']
        addl_info_df = addl_info_df[cols_to_include].rename(columns={'CATEGORY_NAME': 'name'})

        self.ftr_summary_df = rf_df.merge(addl_info_df, how='left', on='name').copy()

    ##############################
    ### output
    ##############################

    def _generate_plots(self, obj_list=['Freq_rel', 'Sev_rel', 'LC_rel', 'LR_rel']):
        if not os.path.exists(PLOTS_DIR_PATH):
            os.makedirs(PLOTS_DIR_PATH)

        for ftr in self.ftr_info.keys():
            ftr_nm = self.ftr_info[ftr]['name']

            # basic univariates
            for obj in obj_list:
                plt.ioff()
                fig, axs = plt.subplots(figsize=(9, 4))
                df = self.ftr_info[ftr]['univariate']
                sns.barplot(data=df, x=ftr_nm, y='EExp', color='steelblue', alpha=0.5, ax=axs)
                axs2 = axs.twinx()
                sns.pointplot(data=df, x=ftr_nm, y=obj, color='black', ax=axs2)
                plt.savefig(f"{PLOTS_DIR_PATH}/{self.dv_name}_univariate_{ftr_nm}_{obj}.png")
                plt.clf()

            # relativites by hue... try/except becasue if primary=secondary, it will blow up.
            for obj in obj_list:
                for sec_var in self.ftr_info[ftr]['secondary_univariate'].keys():
                    try:
                        plt.ioff()
                        fig, axs = plt.subplots(figsize=(9, 4))
                        df = self.ftr_info[ftr]['secondary_univariate'][sec_var]
                        sns.pointplot(data=df, x=ftr, y=obj, hue=sec_var, ax=axs)
                        axs.set_ylim(0, None)
                        axs.set_title(f'{self.dv_name}: {ftr} - {obj}')
                        plt.savefig(f"{PLOTS_DIR_PATH}/{self.dv_name}_bivariate_{ftr_nm}_{sec_var}_{obj}.png")
                        plt.clf()
                    except:
                        pass

    ##############################
    ### output
    ##############################

    def _format_it(self, workbook, worksheet, df, df_startrow, df_startcol, obj_to_format, col_format_dict,
                   gradient_entire_range=False, magic_underlines=False):

        my_white = '#ffffff'
        my_red = '#ff0000'

        underline_format = workbook.add_format()
        underline_format.set_bottom()

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
            cell_range = xl_range_abs(first_row + 1, first_col + 1, last_row, last_col)
            worksheet.conditional_format(cell_range,
                                         {'type': '2_color_scale', 'min_color': my_white, 'max_color': my_red})

        # to underline when first column changes
        if magic_underlines:
            # ignore the first column
            cell_range = xl_range_abs(first_row + 1, first_col, last_row, last_col - 1)
            worksheet.conditional_format(
                cell_range, {'type': 'formula',
                             'criteria': f'=$B{first_row + 2}<>$B{first_row + 3}',
                             'format': underline_format})

        # zoom it
        worksheet.set_zoom(80)

    def export_summary(self, filename, obj_to_format, stats_formatting=INS_STATS_FORMATTING_DICT):
        # formatting defaults
        DEFAULT_START_ROW = 2
        DEFAULT_START_COL = 2
        INTRA_TABLE_PADDING = 5
        CHART_ROW_PADDING = 16

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        workbook = writer.book

        # control_totals
        new_start_row = DEFAULT_START_ROW
        for sec_var, sec_uni in self.secondary_control_totals.items():
            sec_uni.to_excel(writer, sheet_name="controls", startrow=new_start_row, startcol=DEFAULT_START_COL,
                             index=False)
            worksheet = writer.sheets["controls"]
            self._format_it(workbook, worksheet,
                            df=sec_uni, df_startrow=new_start_row, df_startcol=DEFAULT_START_COL,
                            obj_to_format=obj_to_format,
                            col_format_dict=stats_formatting
                            )
            new_start_row = new_start_row + sec_uni.shape[0] + INTRA_TABLE_PADDING

        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # main variable tab
        self.ftr_summary_df.to_excel(writer, sheet_name="variables", startrow=DEFAULT_START_ROW,
                                     startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["variables"]
        for idx, rf in enumerate(self.ftr_summary_df['name'].tolist()):
            this_sheet = f"rf_{str(idx)}"
            worksheet.write_url(DEFAULT_START_ROW + 1 + idx, DEFAULT_START_COL, f'internal: {this_sheet}!A1', string=rf)
        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # individidual risk factor exhibits
        indiv_start_row = DEFAULT_START_ROW + CHART_ROW_PADDING
        for idx, rf in enumerate(self.ftr_summary_df['name'].tolist()):
            this_sheet = f"rf_{str(idx)}"

            # univariate stats... beneath them put secondary-level univariates
            uni_df = self.ftr_info[rf]['univariate']
            uni_df.to_excel(writer, sheet_name=this_sheet, startrow=indiv_start_row, startcol=DEFAULT_START_COL,
                            index=False)
            worksheet = writer.sheets[this_sheet]
            self._format_it(workbook, worksheet,
                            df=uni_df, df_startrow=indiv_start_row, df_startcol=DEFAULT_START_COL,
                            obj_to_format=obj_to_format,
                            col_format_dict=stats_formatting
                            )
            new_start_row = indiv_start_row + uni_df.shape[0] + INTRA_TABLE_PADDING

            # secondary univariates (immediately below univariate stats)
            for sec_var, sec_ftr_stats_df in self.ftr_info[rf]['secondary_univariate'].items():
                sec_ftr_stats_df.to_excel(writer, sheet_name=this_sheet, startrow=new_start_row,
                                          startcol=DEFAULT_START_COL - 1, index=False)  # extra col!!
                worksheet = writer.sheets[this_sheet]
                self._format_it(workbook, worksheet,
                                df=sec_ftr_stats_df, df_startrow=new_start_row, df_startcol=DEFAULT_START_COL - 1,
                                obj_to_format=obj_to_format + ['EExp'],
                                col_format_dict=stats_formatting,
                                magic_underlines=True
                                )
                new_start_row = new_start_row + sec_ftr_stats_df.shape[0] + INTRA_TABLE_PADDING

            # exposure distribution by secondary variables
            new_start_row = indiv_start_row
            new_start_col = DEFAULT_START_COL + uni_df.shape[1] + 1
            for sec_var, exp_distn_df in self.ftr_info[rf]['exp_distn'].items():
                exp_distn_df.to_excel(writer, sheet_name=this_sheet, startrow=new_start_row, startcol=new_start_col,
                                      index=True)
                worksheet = writer.sheets[this_sheet]
                self._format_it(workbook, worksheet,
                                df=exp_distn_df, df_startrow=new_start_row, df_startcol=new_start_col,
                                obj_to_format=obj_to_format,
                                col_format_dict={col: '0.00%' for col in exp_distn_df.columns[1:]},
                                gradient_entire_range=True
                                )
                new_start_row = new_start_row + exp_distn_df.shape[0] + INTRA_TABLE_PADDING

            worksheet.set_zoom(70)
            worksheet.hide_gridlines(2)
            worksheet.write_url('A1', 'internal: variables!A1', string="variables")

            # for each feature, add the simple objective charts # TODO: drive this off the formatted relativities
            for idx, obj in enumerate(['LR_rel', 'LC_rel', 'Sev_rel', 'Freq_rel']):
                row_nbr = 1
                col_nbr = 3 + (7 * idx)
                col_letter = xl_col_to_name(col_nbr)
                # some combinations won't have a chart (primary=secondary)... so just let it continue
                try:
                    worksheet.insert_image(f'{col_letter}{row_nbr}',
                                           f"{PLOTS_DIR_PATH}/{self.dv_name}_univariate_{rf}_{obj}.png",
                                           {'x_scale': 0.7, 'y_scale': 0.7})
                except:
                    pass

            # # for each feature, add the objective charts for each objective (if exists)
            # for var_idx, sec_var in enumerate(self.secondary_var_list):
            #     for obj_idx, obj in enumerate(['Avg_Loss_rel', 'Avg_Eval_rel', 'Ratio_rel']):
            #         row_nbr = 1 + (var_idx + 1) * 16
            #         col_nbr = 3 + (7 * obj_idx)  # had been 6
            #         col_letter = xl_col_to_name(col_nbr)
            #         # some combinations won't have a chart (primary=secondary)... so just let it continue
            #         try:
            #             worksheet.insert_image(f'{col_letter}{row_nbr}',
            #                                    f"{PLOTS_DIR_PATH}/{self.dv_name}_bivariate_{rf}_{sec_var}_{obj}.png",
            #                                    {'x_scale': 0.75, 'y_scale': 0.75})
            #         except:
            #             pass
        writer.save()
