import pandas as pd
import math
import random
import string

import matplotlib.pyplot as plt
import seaborn as sns

from xlsxwriter.utility import xl_col_to_name, xl_range_abs

PLOT_DIR = './plots/'


def apply_ntiles(s, num_ntiles):
    # determine domain values corresponding to desired percentiles... then use cut() instead of qcut() for consistency
    pctile_list = [pctiles / num_ntiles for pctiles in range(num_ntiles + 1)]
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_percentiles(s, pctile_list):
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_fixed_cutpoints(s, fixed_cutpoints):
    if fixed_cutpoints[-1] == s.max():
        fixed_cutpoints[-1] = fixed_cutpoints[-1] + 0.01
    elif fixed_cutpoints[-1] < s.max():
        fixed_cutpoints.append(s.max() + 0.01)

    return pd.cut(s, bins=fixed_cutpoints, right=False, include_lowest=True, duplicates='drop')


def apply_stand_alone_values(s, stand_alone_list, fallback_text="everything_else"):
    s2 = s.copy()
    in_stand_alone_idx = s2.isin(stand_alone_list)
    s2.loc[~in_stand_alone_idx] = fallback_text
    return s2


def return_binned_series(s, bin_info, fallback_text="everything_else"):
    bin_method, bin_param = bin_info
    if bin_method == 'num_ntiles':
        bin_s = apply_ntiles(s, bin_param)
    elif bin_method == 'pctile_list':
        bin_s = apply_percentiles(s, bin_param)
    elif bin_method == 'fixed_cutpoints':
        bin_s = apply_fixed_cutpoints(s, bin_param)
    elif bin_method == 'round':
        bin_s = s.round(bin_param)
    elif bin_method == 'cat_stand_alone_values':
        bin_s = apply_stand_alone_values(s, bin_param, fallback_text)
    else:
        bin_s = s
    return bin_s


def get_series_info(s):
    info_dict = {
        'distinct_val': s.nunique(),
        'missing_pct': pd.isna(s).sum() / s.shape[0],
        'concentration_pct': s.value_counts(dropna=False).iloc[0] / s.shape[0]
    }

    s_info = pd.Series(info_dict)
    s_info.name = s.name

    return s_info


def grab_data_type(s):
    # just getting the data type for a series
    return s.dtype.name


def grab_num_distinct_values(s):
    # just getting number of unique values for a series
    return s.nunique()


def bin_logic(s, ftr_bin_info=None, ord_max_stand_alone_values=20, default_num_ntiles=8, cat_max_stand_alone_values=30,
              cat_pct_to_stand_alone=0.03):
    # if binning info is passed in for the feature, use it.
    if ftr_bin_info:
        return return_binned_series(s, ftr_bin_info)
    # otherwise, apply some default binning based on type & number of distinct values.  Idea is to do SOME binning
    else:
        data_type = grab_data_type(s)
        num_distinct = grab_num_distinct_values(s)
        if data_type == 'object':
            if num_distinct <= cat_max_stand_alone_values:
                return s
            else:
                cat_pct_per_value = s.value_counts(normalize=True)
                cat_stand_alone_value_list = list(cat_pct_per_value[cat_pct_per_value >= cat_pct_to_stand_alone].index)
                return return_binned_series(s, ('cat_stand_alone_values', cat_stand_alone_value_list))
        else:  # data type is ordinal
            if num_distinct <= ord_max_stand_alone_values:
                return s
            else:
                return return_binned_series(s, ('num_ntiles', default_num_ntiles))


def apply_binning_to_df(df, ftr_name, ftr_bin_info=None, ord_max_stand_alone_values=20, default_num_ntiles=8,
                        cat_max_stand_alone_values=30, cat_pct_to_stand_alone=0.03):
    # apply the binning logic to one column of the dataframe... return dataframe with BINNED values for the "ftr_name" column

    binned_ftr = bin_logic(df[ftr_name], ftr_bin_info, ord_max_stand_alone_values, default_num_ntiles,
                           cat_max_stand_alone_values, cat_pct_to_stand_alone)
    all_cols_but_ftr_name = [col for col in df.columns if col != ftr_name]
    return pd.concat([df[all_cols_but_ftr_name], binned_ftr], axis=1)


def get_sub_cols(ftr_name, peril_cc, peril_il, base_cols):
    # to run quicker, want to skinny down the dataframe that's being used in the functions
    return base_cols + [ftr_name, peril_cc, peril_il]


def generate_stats(df, peril_abbr, peril_cc, peril_il, ftr_name, stat_function, stat_function_base_cols,
                   ftr_bin_info=None, ord_max_stand_alone_values=20, default_num_ntiles=8,
                   cat_max_stand_alone_values=30, cat_pct_to_stand_alone=0.03
                   ):
    # generate univariate stats for a given feature/peril/aggregation function
    sub_cols = get_sub_cols(ftr_name, peril_cc, peril_il, stat_function_base_cols)
    df_for_stats = apply_binning_to_df(df[sub_cols].copy(), ftr_name, ftr_bin_info, ord_max_stand_alone_values,
                                       default_num_ntiles, cat_max_stand_alone_values, cat_pct_to_stand_alone)
    return df_for_stats.groupby(ftr_name).apply(
        lambda x: stat_function(x, peril_abbr, peril_cc, peril_il)).reset_index()


def calculate_signal(uni_df, book_totals, signal_metric_col, signal_volume_col='house_years'):
    # restate totals... since incoming df may have already been filtered
    book_metric = book_totals[signal_metric_col]
    book_exposure = book_totals[signal_volume_col]

    df2 = uni_df.copy()
    df2['wgt_SSE'] = df2.apply(
        lambda x: x[signal_metric_col] * (x[signal_metric_col] - book_metric) * (x[signal_metric_col] - book_metric),
        axis=1)
    signal = math.pow(df2['wgt_SSE'].sum() / book_exposure, 0.5) / book_metric
    return signal


def generate_random_string(n=8):
    # generate unique filename for each plot... associate it with the feature name to make display easier
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def format_column_headers(writer, worksheet, col_list, start_row, start_col):
    workbook = writer.book

    cell_format = workbook.add_format()

    cell_format.set_pattern(1)  # This is optional when using a solid fill.
    cell_format.set_bg_color('#42b6f5')

    cell_format.set_font_color('white')
    cell_format.set_bold()

    cell_format.set_bottom(1)
    cell_format.set_top(1)
    cell_format.set_left(1)
    cell_format.set_right(1)

    for col_idx, col in enumerate(col_list):
        worksheet.write(start_row, start_col + col_idx, col, cell_format)
    return worksheet


def format_data_values(workbook, worksheet, df, df_startrow, df_startcol, col_type_dict={}, col_cond_format_list=[]):
    first_row = df_startrow
    first_col = df_startcol
    last_row = df_startrow + df.shape[0]
    last_col = df_startcol + df.shape[1]

    # number format
    for col, format_string in col_type_dict.items():
        the_format = workbook.add_format({'num_format': format_string})
        if col in df.columns.tolist():
            col_idx = df.columns.tolist().index(col)
            col_nbr = df_startcol + col_idx
            col_letter = xl_col_to_name(col_nbr)
            worksheet.set_column(f'{col_letter}:{col_letter}', 20, the_format)

    # columns to conditionally format
    my_white = '#ffffff'
    my_red = '#ff0000'
    for cond_format_col in col_cond_format_list:
        if cond_format_col in df.columns.tolist():
            obj_col_idx = df.columns.tolist().index(cond_format_col)
            col_nbr = df_startcol + obj_col_idx
            cell_range = xl_range_abs(first_row, col_nbr, last_row, col_nbr)
            worksheet.conditional_format(cell_range,
                                         {'type': '2_color_scale', 'min_color': my_white, 'max_color': my_red})


class PerilAnalysis:
    def __init__(self,
                 df, column_list_to_consider,
                 peril_abbr,
                 peril_cc, peril_il, stat_function, stat_function_base_cols,
                 signal_metric_col, signal_volume_col,
                 ord_max_stand_alone_values=20, default_num_ntiles=8,
                 cat_max_stand_alone_values=30, cat_pct_to_stand_alone=0.03
                 ):
        self.df = df
        self.column_list_to_consider = column_list_to_consider
        self.peril_abbr = peril_abbr
        self.peril_cc = peril_cc
        self.peril_il = peril_il
        self.stat_function = stat_function
        self.stat_function_base_cols = stat_function_base_cols
        self.signal_metric_col = signal_metric_col
        self.signal_volume_col = signal_volume_col
        self.ord_max_stand_alone_values = ord_max_stand_alone_values
        self.default_num_ntiles = default_num_ntiles
        self.cat_max_stand_alone_values = cat_max_stand_alone_values
        self.cat_pct_to_stand_alone = cat_pct_to_stand_alone

        self.usage_summary_df = self.get_usage_summary()
        self.peril_exhibits = self.process_peril()

    def get_usage_summary(self):
        summary_info_dict = {}
        for col in self.column_list_to_consider:
            summary_info_dict[col] = get_series_info(self.df[col])

        summary_df = pd.DataFrame(data=summary_info_dict).T
        summary_df['data_type'] = self.df[self.column_list_to_consider].dtypes.astype(str)  # add data type
        summary_df.reset_index(inplace=True, names='column')
        return summary_df[['column', 'data_type', 'distinct_val', 'missing_pct', 'concentration_pct']]

    def generate_plot(self, stats_df, ftr_name, show_plot=False):
        plt.ioff()

        fig, axs = plt.subplots(figsize=(20, 4))
        sns.barplot(data=stats_df, x=ftr_name, y=self.signal_volume_col, color='steelblue', ax=axs)
        axs2 = axs.twinx()
        sns.pointplot(data=stats_df, x=ftr_name, y=self.signal_metric_col, color='black', ax=axs2)

        plot_filename = generate_random_string()
        plt.savefig(f"{PLOT_DIR}{plot_filename}.png")
        if show_plot:
            plt.show()
        plt.clf()

        return plot_filename

    def process_peril(self):

        df_stats = {}
        peril_signals = {}
        plot_names = {}
        overall_peril_totals = self.stat_function(self.df, self.peril_abbr, self.peril_cc, self.peril_il)

        for ftr_name in self.column_list_to_consider:
            col_peril_stats = generate_stats(
                df=self.df,
                peril_abbr=self.peril_abbr,
                peril_cc=self.peril_cc,
                peril_il=self.peril_il,
                ftr_name=ftr_name,
                stat_function=self.stat_function,
                stat_function_base_cols=self.stat_function_base_cols,
                ftr_bin_info=None,  # Run with defaults
                ord_max_stand_alone_values=self.ord_max_stand_alone_values,
                default_num_ntiles=self.default_num_ntiles,
                cat_max_stand_alone_values=self.cat_max_stand_alone_values,
                cat_pct_to_stand_alone=self.cat_pct_to_stand_alone
            )
            df_stats[ftr_name] = col_peril_stats
            peril_signals[ftr_name] = calculate_signal(
                uni_df=col_peril_stats,
                book_totals=overall_peril_totals,
                signal_metric_col=self.signal_metric_col,
                signal_volume_col=self.signal_volume_col
            )
            plot_names[ftr_name] = self.generate_plot(
                stats_df=col_peril_stats,
                ftr_name=ftr_name,
                show_plot=False
            )
        return {
            'stats': df_stats,
            'signals': pd.Series(peril_signals),
            'plot_names': plot_names
        }

    def inspect_ftr(self, ftr_name):
        print(f"signal for {ftr_name}: {self.peril_exhibits['signals'][ftr_name]}")
        self.generate_plot(
            stats_df=self.peril_exhibits['stats'][ftr_name],
            ftr_name=ftr_name,
            show_plot=True
        )
        return self.peril_exhibits['stats'][ftr_name]

    def update_ftr(self, ftr_name, ftr_bin_info=None):

        col_peril_stats = generate_stats(
            df=self.df,
            peril_abbr=self.peril_abbr,
            peril_cc=self.peril_cc,
            peril_il=self.peril_il,
            ftr_name=ftr_name,
            stat_function=self.stat_function,
            stat_function_base_cols=self.stat_function_base_cols,
            ftr_bin_info=ftr_bin_info,  # Use what user just specified
            ord_max_stand_alone_values=self.ord_max_stand_alone_values,
            default_num_ntiles=self.default_num_ntiles,
            cat_max_stand_alone_values=self.cat_max_stand_alone_values,
            cat_pct_to_stand_alone=self.cat_pct_to_stand_alone
        )
        self.peril_exhibits['stats'][ftr_name] = col_peril_stats

        overall_peril_totals = self.stat_function(self.df, self.peril_abbr, self.peril_cc, self.peril_il)
        self.peril_exhibits['signals'][ftr_name] = calculate_signal(
            uni_df=col_peril_stats,
            book_totals=overall_peril_totals,
            signal_metric_col=self.signal_metric_col,
            signal_volume_col=self.signal_volume_col
        )
        print(f"signal for {ftr_name}: {self.peril_exhibits['signals'][ftr_name]}")

        self.peril_exhibits['plot_names'][ftr_name] = self.generate_plot(
            stats_df=col_peril_stats,
            ftr_name=ftr_name,
            show_plot=True
        )

        return self.peril_exhibits['stats'][ftr_name]

    def export_peril_exhibits(self, results_filename, col_type_dict={}, col_cond_format_list=[]):
        # formatting defaults
        DEFAULT_START_ROW = 2
        DEFAULT_START_COL = 1
        COL_PADDING = 3
        CHART_ROW_PADDING = 20
        COLUMN_WIDTH = 25

        writer = pd.ExcelWriter(results_filename, engine='xlsxwriter')
        workbook = writer.book

        # variable summary
        this_start_row = DEFAULT_START_ROW

        summary_df = self.usage_summary_df.copy()
        signals_series = pd.Series(self.peril_exhibits['signals'])
        signals_series.name = f'signal_{self.signal_metric_col}'
        summary_df = summary_df.merge(signals_series, how='left', left_on='column', right_index=True).dropna(
            subset=f'signal_{self.signal_metric_col}').copy()

        summary_df.to_excel(writer, sheet_name='columns', startrow=this_start_row, startcol=DEFAULT_START_COL,
                            index=False)
        worksheet = writer.sheets["columns"]
        worksheet = format_column_headers(writer, worksheet, summary_df.columns.tolist(), this_start_row,
                                          DEFAULT_START_COL)
        format_data_values(workbook, worksheet, summary_df, this_start_row, DEFAULT_START_COL,
                           {'missing_pct': '0.0%', f'signal_{self.signal_metric_col}': '0.0000%'},
                           ['missing_pct', f'signal_{self.signal_metric_col}'])

        for idx, col in enumerate(list(summary_df['column'].tolist())):
            this_sheet = f"col_{str(idx)}"
            worksheet.write_url(this_start_row + 1 + idx, DEFAULT_START_COL, f'internal: {this_sheet}!A1', string=col)

        # individual risk factor exhibits
        indiv_start_row = DEFAULT_START_ROW + CHART_ROW_PADDING
        for idx, col in enumerate(summary_df['column'].tolist()):
            this_sheet = f"col_{str(idx)}"

            # one-way stats
            uni_df = self.peril_exhibits['stats'][col]
            uni_df.to_excel(writer, sheet_name=this_sheet, startrow=indiv_start_row, startcol=DEFAULT_START_COL,
                            index=False)
            worksheet = writer.sheets[this_sheet]
            worksheet.set_column('B:Z', COLUMN_WIDTH)

            worksheet = format_column_headers(writer, worksheet, uni_df.columns.tolist(), indiv_start_row,
                                              DEFAULT_START_COL)
            format_data_values(workbook, worksheet, uni_df, indiv_start_row, DEFAULT_START_COL, col_type_dict,
                               col_cond_format_list)

            worksheet.set_zoom(70)
            worksheet.hide_gridlines(2)
            try:
                filename = self.peril_exhibits['plot_names'][col]
                worksheet.insert_image('C1', f"{PLOT_DIR}{filename}.png")
            except:
                pass
            worksheet.write_url('A1', 'internal: columns!A1', string="columns")

        writer.save()
