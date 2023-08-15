import pandas as pd
from datetime import datetime
from .api_batch import ApiBatch
from .report import Report

from .config.config import BASE_REPORT_CONFIG, DEFAULT_EXCEPTION_COLS, REPORT_TRANSLATION_TABLES,\
    EXCLUDE_GEO_ERRORS_CONDITION, BATCH_DATA_DICTIONARY
from .utils.excel_utils import format_column_headers, format_true_values_in_summary
from .utils.stat_utils import default_agg_fcn

DEFAULT_START_ROW = 2
DEFAULT_START_COL = 2


def _get_report_exception_count(exhibit_dict):
    try:
        return exhibit_dict['exception_summary']['num_exceptions'].sum()
    except KeyError:
        return None


def _generate_exception_summary(report_dict):
    return pd.DataFrame({
        'report_name': report_dict.keys(),
        'num_exceptions': [_get_report_exception_count(report_obj.exhibits_dict) for (report_name, report_obj) in
                           report_dict.items()]
    }
    )


def write_summary(writer, summary_df):
    cols_to_exclude=['exclude_geo_errors', 'column_list', 'bin_variables']
    cols_to_keep=[col for col in summary_df.columns if col not in cols_to_exclude]
    summary_df[cols_to_keep].to_excel(writer, sheet_name='reports', startrow=DEFAULT_START_ROW,
                                      startcol=DEFAULT_START_COL, index=False)
    worksheet = writer.sheets["reports"]
    worksheet = format_column_headers(writer, worksheet, cols_to_keep, DEFAULT_START_ROW, DEFAULT_START_COL)
    worksheet = format_true_values_in_summary(writer, worksheet, DEFAULT_START_ROW, DEFAULT_START_COL,
                                              summary_df[cols_to_keep].shape)
    for idx, report_name in enumerate(summary_df['report_name'].tolist()):
        worksheet.write_url(DEFAULT_START_ROW + 1 + idx, DEFAULT_START_COL, f'internal: {report_name}!A1',
                            string=report_name)

    worksheet.set_zoom(80)
    worksheet.hide_gridlines()
    return writer


def write_exceptions(writer, exceptions_df):
    exceptions_df.to_excel(writer, sheet_name='exceptions', startrow=DEFAULT_START_ROW, startcol=DEFAULT_START_COL,
                           index=False)
    worksheet = writer.sheets["exceptions"]
    worksheet = format_column_headers(writer, worksheet, exceptions_df.columns.tolist(), DEFAULT_START_ROW, DEFAULT_START_COL)
    worksheet.set_zoom(80)
    worksheet.hide_gridlines()
    return writer


def load_report_translations(translation_filename):
    if translation_filename:
        return pd.read_excel(translation_filename, sheet_name=None)
    else:
        return REPORT_TRANSLATION_TABLES


class PortfolioAnalysis:
    def __init__(self, analysis_name, batch_filepath,
                 batch_num_rows=None,
                 agg_fcn=None,
                 agg_fcn_input_list=None,
                 user_report_config=None,
                 user_exception_column_list=None,
                 max_records_per_exception=None,
                 report_translation_dict=None,
                 batch_data_dictionary=None,
                 apply_data_fixes=True
                 ):
        # read input
        self.analysis_name = analysis_name
        self.batch_filepath = batch_filepath

        self.batch_num_rows = batch_num_rows
        self.agg_fcn = agg_fcn if agg_fcn else default_agg_fcn
        self.agg_fcn_input_list = [] if agg_fcn_input_list is None else agg_fcn_input_list
        self.report_config = BASE_REPORT_CONFIG if user_report_config is None else user_report_config
        self.user_exception_column_list = [] if user_exception_column_list is None else user_exception_column_list
        self.max_records_per_exception = max_records_per_exception
        self.report_translation_dict = REPORT_TRANSLATION_TABLES if report_translation_dict is None else report_translation_dict
        self.batch_data_dictionary = BATCH_DATA_DICTIONARY if batch_data_dictionary is None else batch_data_dictionary
        self.apply_data_fixes = apply_data_fixes

        # instantiate the API batch object (which cleans batch data)
        self.batch_obj = ApiBatch(
            self.read_batch_file(),
            apply_data_fixes=self.apply_data_fixes
        )

        # report config file for the portfolio analysis
        self.report_dict = self.generate_reports()

        # summarize portfolio analysis
        self.summary_df = self.create_summary_report()
        self.exception_df = self.create_exception_report()

        # write the portfolio analysis report
        self.write_portfolio_analysis_report()

    def read_batch_file(self):
        if self.batch_num_rows:
            return pd.read_csv(self.batch_filepath, nrows=self.batch_num_rows)
        else:
            return pd.read_csv(self.batch_filepath)

    def dedup_keep_order(self, big_list):
        dedup_list = []
        for item in big_list:
            if item not in dedup_list:
                dedup_list.append(item)
        return dedup_list

    def generate_reports(self):
        # generate reports
        report_dict = {}
        for idx, row in self.report_config.iterrows():
            report_name = row['report_name']
            cols_to_include = self.dedup_keep_order(row['column_list'] + self.user_exception_column_list + self.agg_fcn_input_list)
            bin_vars = row['bin_variables']
            exclude_geo_errors = row['exclude_geo_errors']
            cols_missing_from_batch = set(cols_to_include).difference(set(self.batch_obj.df.columns))
            if len(cols_missing_from_batch) == 0:
                if exclude_geo_errors:
                    report_dict[report_name] = Report(
                        report_name,
                        self.batch_obj.df.query(EXCLUDE_GEO_ERRORS_CONDITION)[cols_to_include],
                        agg_fcn=self.agg_fcn,
                        agg_fcn_input_list=self.agg_fcn_input_list,
                        bin_cols=bin_vars,
                        report_trans_dict=self.report_translation_dict,
                        batch_data_dictionary=self.batch_data_dictionary,
                        user_exception_column_list=self.user_exception_column_list,
                        max_records_per_exception=self.max_records_per_exception
                    )
                else:
                    report_dict[report_name] = Report(
                        report_name,
                        self.batch_obj.df[cols_to_include],
                        agg_fcn=self.agg_fcn,
                        agg_fcn_input_list=self.agg_fcn_input_list,
                        bin_cols=bin_vars,
                        report_trans_dict=self.report_translation_dict,
                        batch_data_dictionary=self.batch_data_dictionary,
                        user_exception_column_list=self.user_exception_column_list,
                        max_records_per_exception=self.max_records_per_exception
                    )

            else:
                print(f"skipping report {report_name} since batch is missing columns: {cols_missing_from_batch}")
        return report_dict

    def create_summary_report(self):
        summary_df = _generate_exception_summary(self.report_dict).merge(self.report_config, how='left', on='report_name')
        final_cols = ['column_list', 'bin_variables']
        new_col_order = [col for col in summary_df.columns if col not in final_cols] + final_cols
        return summary_df[new_col_order]

    def determine_exception_cols(self):
        e_cols = [col for col in DEFAULT_EXCEPTION_COLS if col in self.batch_obj.df.columns]
        user_cols = self.user_exception_column_list
        return user_cols + [col for col in e_cols if col not in user_cols]

    def create_exception_report(self):
        exception_record_list = []
        e_cols_to_user = self.determine_exception_cols()
        for report_name, report_obj in self.report_dict.items():
            if report_obj.exhibits_dict['exception_summary'].shape[0] > 0:
                for idx, exception in report_obj.exhibits_dict['exception_summary'].query(
                        "num_exceptions > 0").iterrows():
                    this_exception_df = self.batch_obj.df.query(exception.rule_logic)[e_cols_to_user]
                    if self.max_records_per_exception and self.max_records_per_exception < this_exception_df.shape[0]:
                        print(f"truncate exceptions for {report_name}")
                        this_exception_df = this_exception_df.iloc[:self.max_records_per_exception]
                    exception_record_list.append(this_exception_df)
        return pd.concat(exception_record_list).drop_duplicates()

    def write_portfolio_analysis_report(self):
        pa_report_name = f"PortfolioAnalysis_{self.analysis_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        writer = pd.ExcelWriter(pa_report_name, engine='xlsxwriter')
        writer = write_summary(writer, self.summary_df)
        writer = write_exceptions(writer, self.exception_df)
        for report_name, report_obj in self.report_dict.items():  # TODO: How to customize report output?
            writer = report_obj.write_report_sheet(writer)
        writer.save()



