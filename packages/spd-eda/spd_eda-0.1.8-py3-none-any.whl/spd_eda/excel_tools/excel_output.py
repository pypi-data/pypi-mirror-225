import pandas as pd
from xlsxwriter.utility import xl_range_abs, xl_col_to_name

COL_PADDING = 3
ROW_PADDING = 3


def format_ws(workbook, worksheet, df, df_startrow, df_startcol, col_type_dict={}, df_includes_index=False,
              col_cond_format_list=[], gradient_entire_range=False, magic_underlines=False):

    if df_includes_index:
        df_startcol = df_startcol + 1

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

    # for entire range
    if gradient_entire_range:
        # ignore the first column
        cell_range = xl_range_abs(first_row, first_col + 1, last_row, last_col)
        worksheet.conditional_format(cell_range,
                                     {'type': '2_color_scale', 'min_color': my_white, 'max_color': my_red})

    # to underline when first column changes
    underline_format = workbook.add_format()
    underline_format.set_bottom()

    if magic_underlines:
        # ignore the first column
        cell_range = xl_range_abs(first_row + 1, first_col, last_row, last_col - 1)
        worksheet.conditional_format(
            cell_range, {'type': 'formula',
                         'criteria': f'=$B{first_row + 3}<>0',  # TODO: parameterize the first grouped column
                         'format': underline_format})
    # zoom it
    worksheet.set_zoom(80)


class ExcelExport:
    def __init__(self, filename, control_df_list, col_summary_df, var_info_dict, col_type_dict={},
                 col_cond_format_list=[], def_start_row=2, def_start_col=2, row_padding=3):
        self.filename = filename

        self.control_df_list = control_df_list
        self.col_summary_df = col_summary_df
        self.var_info_dict = var_info_dict

        self.col_type_dict = col_type_dict
        self.col_cond_format_list = col_cond_format_list

        self.def_start_row = def_start_row
        self.def_start_col = def_start_col
        self.row_padding = row_padding

        self.write_it()

    def write_it(self):
        writer = pd.ExcelWriter(self.filename, engine='xlsxwriter')
        workbook = writer.book

        # control totals
        this_start_row = self.def_start_row
        for control_df in self.control_df_list:
            control_df.to_excel(writer, sheet_name='control', startrow=this_start_row, startcol=self.def_start_col,
                                index=True)
            worksheet = writer.sheets['control']
            format_ws(workbook, worksheet, control_df, this_start_row, self.def_start_col,
                      col_type_dict=self.col_type_dict, df_includes_index=True,
                      col_cond_format_list=self.col_cond_format_list)
            this_start_row = this_start_row + control_df.shape[0] + self.row_padding

        # variable summary df
        this_start_row = self.def_start_row
        self.col_summary_df.to_excel(writer, sheet_name='columns', startrow=this_start_row,
                                     startcol=self.def_start_col, index=True)
        worksheet = writer.sheets["columns"]
        for idx, col in enumerate(list(self.col_summary_df.index)):
            this_sheet = f"col_{str(idx)}"
            worksheet.write_url(self.def_start_row + 1 + idx, self.def_start_col, f'internal: {this_sheet}!A1',
                                string=col)

        # individual worksheets
        for idx, col in enumerate(list(self.col_summary_df.index)):
            this_start_row = self.def_start_row
            this_sheet = f"col_{str(idx)}"
            indiv_col_df = self.var_info_dict[col]['one_way']
            indiv_col_df.to_excel(writer, sheet_name=this_sheet, startrow=this_start_row, startcol=self.def_start_col,
                                  index=True)
            worksheet = writer.sheets[this_sheet]
            worksheet.write_url('A1', 'internal: columns!A1', string="columns")
            format_ws(workbook, worksheet, indiv_col_df, this_start_row, self.def_start_col,
                      col_type_dict=self.col_type_dict, df_includes_index=True,
                      col_cond_format_list=self.col_cond_format_list)

            # if bi-variate distributions exist (using secondary variable)... print them
            bi_start_row = this_start_row + indiv_col_df.shape[0] + ROW_PADDING
            for addl_exhibits in self.var_info_dict[col].keys():
                if 'bivariate_stats_' in addl_exhibits:
                    bivariate_stats_df = self.var_info_dict[col][addl_exhibits]
                    bivariate_stats_df.to_excel(writer, sheet_name=this_sheet, startrow=bi_start_row,
                                                startcol=self.def_start_col-1, index=True)  # back it up one column!
                    format_ws(workbook, worksheet, bivariate_stats_df, bi_start_row, self.def_start_col,
                              col_type_dict=self.col_type_dict, df_includes_index=True,
                              col_cond_format_list=self.col_cond_format_list,
                              magic_underlines=True)
                    bi_start_row = bi_start_row + bivariate_stats_df.shape[0] + ROW_PADDING

            # if secondary exposure distributions  exist... print them
            exhibit_start_row = this_start_row
            exhbit_start_col = self.def_start_row + indiv_col_df.shape[1] + COL_PADDING
            for addl_exhibits in self.var_info_dict[col].keys():
                if 'two_way_' in addl_exhibits:
                    exhibit_df = self.var_info_dict[col][addl_exhibits]
                    exhibit_df.to_excel(writer, sheet_name=this_sheet, startrow=exhibit_start_row,
                                          startcol=exhbit_start_col,
                                          index=True)
                    # format with gradient applied to entire df... make everything percentages
                    exhibit_num_format = {col: '0.00%' for col in exhibit_df.columns}
                    format_ws(workbook, worksheet, exhibit_df, exhibit_start_row, exhbit_start_col,
                              col_type_dict=exhibit_num_format, gradient_entire_range=True)
                    # setup for next one
                    exhibit_start_row = exhibit_start_row + exhibit_df.shape[0] + ROW_PADDING

        writer.save()