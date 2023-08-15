import pandas as pd
import awswrangler as wr
from .utils import POSTRGRES_NUMERIC_TYPES, strip_where_from_filter_if_exists
from .athena_column import AthenaColumn


class AthenaTable:
    def __init__(self, db_name, tbl_name):
        self.db_name = db_name
        self.tbl_name = tbl_name
        self.row_count = self.get_row_count()

        self.information_schema = self.get_information_schema()
        self.partition_keys = self.information_schema.query("extra_info == 'partition key'")['column_name'].tolist()

        self.col_info = {}

    def get_sample_records(self, num_rows=10, filter_string="1=1", col_subset_list=[]):
        """

        Parameters
        ----------
        num_rows : optional number of rows to return.  defaults to 10
        filter_string : optional query condition (sql syntax).  defaults to all records, "1=1"
        col_subset_list : optional list of columns to return in result.  defaults to empty list, which return all columns.

        Returns
        -------
        dataframe with sample records from the underlying table

        """

        optional_where_condition = strip_where_from_filter_if_exists(filter_string)
        selected_column_list = "*" if len(col_subset_list) == 0 else ", ".join(col_subset_list)
        SQL = f'SELECT {selected_column_list} from {self.tbl_name} where {optional_where_condition} limit {num_rows}'
        return wr.athena.read_sql_query(SQL, self.db_name)

    def get_row_count(self, filter_string="1=1"):
        """

        Parameters
        ----------
        filter_string : optional query condition (sql syntax).  defaults to all records, "1=1"

        Returns
        -------
        integer value with count of applicable rows

        """

        optional_where_condition = strip_where_from_filter_if_exists(filter_string)
        SQL = f'SELECT count(1) as "n" from {self.tbl_name} where {optional_where_condition}'
        return wr.athena.read_sql_query(SQL, self.db_name).iloc[0]['n']

    def get_information_schema(self):
        # returns information schema for the table
        SQL = f"""
        SELECT column_name, is_nullable, data_type, extra_info
        FROM information_schema.columns
        WHERE table_schema= '{self.db_name}' and table_name = '{self.tbl_name}'
        """
        return wr.athena.read_sql_query(SQL, self.db_name)

    def get_custom_counts(self, custom_expression):
        # returns information schema for the table
        SQL = f"""
        SELECT {custom_expression} as "custom_expr", count(1) as "n"
        FROM {self.tbl_name}
        GROUP BY {custom_expression}
        ORDER BY {custom_expression}
        """
        return wr.athena.read_sql_query(SQL, self.db_name)

    # getting distinct counts is PAINFULLY slow in postgres... so don't automatically call these.
    def _get_distinct_values_for_col(self, col):
        SQL = f'''select count(distinct {col}) as "num_distinct" from {self.tbl_name}'''
        return wr.athena.read_sql_query(SQL, self.db_name).iloc[0]['num_distinct']

    def get_column_summary(self):
        col_summary_df = self.information_schema.copy()
        col_summary_df['distinct_values'] = col_summary_df['column_name'].apply(
            lambda x: self._get_distinct_values_for_col(x))
        return col_summary_df

    def get_records_per_thread_summary(self, thread_list, filter_string="1=1"):
        """
        For a given thread (list of columns), calculate distribution of row counts within these threads.

        For example, if the thread were the set of primary key columns, then each thread would have a single record... and 100% of threads would have a single record.

        This is more useful when threads don't uniquely describe rows & can help answer questions like, "how many records do we typically see for a given company ID (e.g. thread = [Company ID]).

        Parameters
        ----------
        thread_list : list of column names
        filter_string : optional query condition (sql syntax).  defaults to all records, "1=1"

        Returns
        -------
        dataframe showing record counts within threads.

        """
        col_list_as_string = ", ".join(thread_list)
        optional_where_condition = strip_where_from_filter_if_exists(filter_string)
        SQL = f'''
        with tmp as (
                select {col_list_as_string}, count(1) as "recs_in_thread"
                from {self.tbl_name}
                where {optional_where_condition}
                group by {col_list_as_string}
                )
        select recs_in_thread, count(1) as "num_threads", cast(count(1) as REAL) / (select count(1) from tmp) as "pct_threads"
        from tmp
        group by recs_in_thread
        order by recs_in_thread
        '''
        return wr.athena.read_sql_query(SQL, self.db_name)

    def get_thread_examples_with_specified_num_records(self, thread_list, records_per_thread, num_thread_examples=1,
                                                       filter_string="1=1"):
        """
        Use in conjunction with "get_records_per_thread_summary" method.

        Can be helpful to easily identify/inspect examples where a specified number of records occur within a thread.

        Parameters
        ----------
        thread_list : list of column names
        records_per_thread : desired number of records within the thread
        num_thread_examples : number of examples to return.  Defaults to 1.
        filter_string : optional query condition (sql syntax).  defaults to all records, "1=1"

        Returns
        -------
        dataframe containing desired examples.

        """
        col_list_as_string = ", ".join(thread_list)
        optional_where_condition = strip_where_from_filter_if_exists(filter_string)
        a_b_join_string = " and ".join(["a." + t + " = b." + t for t in thread_list])
        a_prefix_string = ",".join(["a." + t for t in thread_list])
        SQL = f'''
        select a.*
        from {self.tbl_name} a
        inner join (
            select {col_list_as_string}, count(1) as "recs_in_thread"
            from {self.tbl_name}
            where {optional_where_condition}
            group by {col_list_as_string}
            having count(1) = {records_per_thread}
            ) b on {a_b_join_string}
        order by {a_prefix_string}
        limit {num_thread_examples * records_per_thread}
        '''
        return wr.athena.read_sql_query(SQL, self.db_name)

    def get_column_info(self):
        # updating the self.col_info dictionary
        for column in self.information_schema['column_name'].tolist():
            print(f"getting column info for: {column}")
            # awkward structure here... fix later
            col_dtype = self.information_schema.query(f"column_name == '{column}'").iloc[0]['data_type']
            if col_dtype in POSTRGRES_NUMERIC_TYPES:
                col_bin_info = {column: {'name': column, 'ord_cat': 'ord', 'bin_strategy': 'top', 'bin_parameter': 20}}
                print(f"use ordinal for {column} since it is {col_dtype}")
            else:
                col_bin_info = {column: {'name': column, 'ord_cat': 'cat', 'bin_strategy': 'top', 'bin_parameter': 20}}
            self.col_info[column] = AthenaColumn(self.db_name, self.tbl_name, column, bin_info=col_bin_info).bin_counts

    def write_summary(self, filename):
        DEFAULT_START_ROW = 5
        DEFAULT_START_COL = 1

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        # workbook = writer.book

        # main column summary
        self.information_schema.to_excel(writer, sheet_name="columns", startrow=DEFAULT_START_ROW,
                                         startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["columns"]
        for idx, col in enumerate(self.information_schema['column_name'].tolist()):
            this_sheet = f"col_{str(idx)}"
            worksheet.write_url(DEFAULT_START_ROW + 1 + idx, DEFAULT_START_COL, f'internal: {this_sheet}!A1',
                                string=col)
        worksheet.set_column('A:Z', 20)

        worksheet.write(1, 1, "Table Name: ")
        worksheet.write(1, 2, self.tbl_name)
        worksheet.write(2, 1, "Record Count: ")
        worksheet.write(2, 2, self.get_row_count())

        worksheet.set_zoom(80)
        worksheet.hide_gridlines(2)

        # sample records
        self.get_sample_records().to_excel(writer, sheet_name="sample", startrow=DEFAULT_START_ROW,
                                           startcol=DEFAULT_START_COL, index=False)
        worksheet = writer.sheets["sample"]

        # column specific information
        for idx, col in enumerate(self.information_schema['column_name'].tolist()):
            this_sheet = f"col_{str(idx)}"
            self.col_info[col].to_excel(writer, sheet_name=this_sheet, startrow=DEFAULT_START_ROW,
                                        startcol=DEFAULT_START_COL, index=False)
            worksheet = writer.sheets[this_sheet]

            worksheet.set_zoom(80)
            worksheet.write_url('A1', 'internal: columns!A1', string="columns")
            worksheet.set_column('A:Z', 20)

        writer.save()
