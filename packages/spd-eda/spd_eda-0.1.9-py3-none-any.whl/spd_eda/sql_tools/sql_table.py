from .connection import Connection

import pandas as pd
from .utils import strip_where_from_opt_filter


class SqlTable:
    def __init__(self, server, db_name, tbl_name):
        self.server = server
        self.db_name = db_name
        self.conn = Connection(self.server, self.db_name).str

        self.tbl_name = tbl_name
        self.row_count = self.get_row_count()
        self.information_schema = self.get_information_schema()

    def get_row_count(self, opt_where="1=1"):
        opt_where = strip_where_from_opt_filter(opt_where)
        sql = 'SELECT count(1) as "n" from {} where {}'.format(self.tbl_name, opt_where)
        return pd.read_sql(sql, self.conn).iloc[0]['n']

    def get_information_schema(self):
        sql = f"select * from information_schema.columns where table_name = '{self.tbl_name}'"
        return pd.read_sql(sql, self.conn)

    def get_sample_records(self, num_rows=10, opt_where="1=1", col_subset_list=[]):
        """
        Parameters
        ----------
        num_rows : optional number of rows to return.  defaults to 10
        opt_where : optional query condition (sql syntax).  defaults to all records, "1=1"
        col_subset_list : optional list of columns to return in result.  defaults to empty list, which return all columns.

        Returns
        -------
        dataframe with sample records from the underlying table

        """

        opt_where = strip_where_from_opt_filter(opt_where)
        selected_column_list = "*" if len(col_subset_list) == 0 else ", ".join(col_subset_list)
        sql = f'SELECT TOP {num_rows} {selected_column_list} from {self.tbl_name} where {opt_where}'
        return pd.read_sql(sql, self.conn)

    def get_records_per_thread_summary(self, thread_list, opt_where="1=1"):
        """
        For a given thread (list of columns), calculate distribution of row counts within these threads.

        For example, if the thread were the set of primary key columns, then each thread would have a single record... and 100% of threads would have a single record.

        This is more useful when threads don't uniquely describe rows & can help answer questions like, "how many records do we typically see for a given company ID (e.g. thread = [Company ID]).

        Parameters
        ----------
        thread_list : list of column names
        opt_where : optional query condition (sql syntax).  defaults to all records, "1=1"

        Returns
        -------
        dataframe showing record counts within threads.

        """
        col_list_as_string = ", ".join(thread_list)
        opt_where = strip_where_from_opt_filter(opt_where)
        sql = f'''
         with tmp as (
                 select {col_list_as_string}, count(1) as "recs_in_thread"
                 from {self.tbl_name}
                 where {opt_where}
                 group by {col_list_as_string}
                 )
         select recs_in_thread, count(1) as "num_threads", cast(count(1) as REAL) / (select count(1) from tmp) as "pct_threads"
         from tmp
         group by recs_in_thread
         order by recs_in_thread
         '''
        return pd.read_sql(sql, self.conn)

    def get_thread_examples_with_specified_num_records(self, thread_list, records_per_thread, num_thread_examples=1,
                                                       opt_where="1=1"):
        """
        Use in conjunction with "get_records_per_thread_summary" method.

        Can be helpful to easily identify/inspect examples where a specified number of records occur within a thread.

        Parameters
        ----------
        thread_list : list of column names
        records_per_thread : desired number of records within the thread
        num_thread_examples : number of examples to return.  Defaults to 1.
        opt_where : optional query condition (sql syntax).  defaults to all records, "1=1"

        Returns
        -------
        dataframe containing desired examples.

        """
        col_list_as_string = ", ".join(thread_list)
        opt_where = strip_where_from_opt_filter(opt_where)
        a_b_join_string = " and ".join(["a." + t + " = b." + t for t in thread_list])
        a_prefix_string = ",".join(["a." + t for t in thread_list])

        sql = f"""
         select top {records_per_thread * num_thread_examples} a.*
         from {self.tbl_name} a
         inner join (
             select {col_list_as_string}, count(1) as "Records_in_Thread"
             from {self.tbl_name}
             where {opt_where}
             group by {col_list_as_string}
             having count(1) = {records_per_thread}
             ) b on {a_b_join_string}
         order by {a_prefix_string}
         """
        return pd.read_sql(sql, self.conn)
