import pandas as pd
from xlsxwriter.utility import xl_range


DEFAULT_START_ROW = 3
DEFAULT_START_COL = 2
ROW_PADDING = 5
COL_PADDING = 3
COL_WIDTH = 20
PLOT_DIR = './plots/'


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
        worksheet.write(start_row, start_col+col_idx, col, cell_format)
    return worksheet


def format_true_values_in_summary(writer, worksheet, start_row, start_col, df_shape):
    workbook = writer.book
    green_format = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
    num_rows, num_cols = df_shape
    first_data_row = start_row+1
    formatted_range = xl_range(first_data_row, start_col, first_data_row + num_rows - 1, start_col + num_cols - 1)
    worksheet.conditional_format(formatted_range,
                                 {"type": "cell", "criteria": "=", "value": "True", "format": green_format}
                                 )
    return worksheet


def format_section_heading(writer, worksheet, heading_text, start_row, start_col):
    workbook = writer.book

    cell_format = workbook.add_format()
    cell_format.set_font_color('red')
    cell_format.set_bold()

    worksheet.write(start_row, start_col, heading_text, cell_format)
    return worksheet


def default_report_sheet(writer, sheet_name, exhibits_dict):

    #####################################
    # FIRST COLUMN OF OUTPUT (raw one-way)
    #####################################
    start_row = DEFAULT_START_ROW
    start_col = DEFAULT_START_COL

    exhibit_key = 'one_way_stats'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            # worksheet.write(start_row-1, start_col-1, "Aggregated Stats")
            worksheet = format_section_heading(writer, worksheet, "DISTRIBUTION", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_col = start_col + df.shape[1] + COL_PADDING

    #####################################
    # SECOND COLUMN OF OUTPUT
    #####################################
    start_row = DEFAULT_START_ROW

    # data dictionary
    exhibit_key = 'dictionary'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            worksheet = format_section_heading(writer, worksheet, "DATA DICTIONARY", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_row = start_row + df.shape[0] + ROW_PADDING

    # usage summary
    exhibit_key = 'usage_summary'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            worksheet = format_section_heading(writer, worksheet, "USAGE SUMMARY", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_row = start_row + df.shape[0] + ROW_PADDING

    # meta data
    exhibit_key = 'metadata'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            worksheet = format_section_heading(writer, worksheet, "TRANSLATIONS", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_row = start_row + df.shape[0] + ROW_PADDING

    # exceptions
    exhibit_key = 'exception_summary'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            worksheet = format_section_heading(writer, worksheet, "EXCEPTIONS", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_row = start_row + df.shape[0] + ROW_PADDING

    # exceptions
    exhibit_key = 'exception_examples'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, startcol=start_col, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            worksheet = format_section_heading(writer, worksheet, "EXCEPTION EXAMPLES", start_row-1, start_col-1)
            worksheet.set_column(start_col, start_col + df.shape[1], COL_WIDTH)
            start_row = start_row + df.shape[0] + ROW_PADDING

    worksheet.write_url('A1', 'internal: reports!A1', string="reports")
    worksheet.set_zoom(80)
    worksheet.hide_gridlines(2)
    return writer


def default_write_sheet(writer, col_name, sheet_name, exhibits_dict):
    # if metadata exists, write it
    start_row = DEFAULT_START_ROW
    exhibit_key = 'translations'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet = format_column_headers(writer, worksheet, df.columns.tolist(), start_row, start_col)
            start_row = start_row + df.shape[0] + ROW_PADDING

    # binned one-way
    exhibit_key = 'bin_one_way'
    if exhibit_key in exhibits_dict.keys():
        df = exhibits_dict[exhibit_key]
        if df.shape[0] > 0:
            df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)
            worksheet = writer.sheets[sheet_name]
            start_row = start_row + df.shape[0] + ROW_PADDING

    # try to write chart
    try:
        worksheet.insert_image('C1', f"{PLOT_DIR}{col_name}.png")
    except:
        pass

    worksheet.set_zoom(80)
    return writer
