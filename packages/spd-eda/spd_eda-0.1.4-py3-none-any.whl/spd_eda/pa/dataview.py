from .config import DB_SERVER
from .connection import Connection
from .pa_stats import PAStats

import pandas as pd


class DataView:
    def __init__(self, db_name, dv_name):
        self.conn = Connection(DB_SERVER, db_name).str
        self.db_name = db_name
        self.dv_name = dv_name

        # get config for data view & instantiate the underlying DataSource class
        self.config = self.get_dv_config()
        self.control_totals = self.get_dv_totals()
        self.experience_period = f"[{self.control_totals['GROUP_ID'].tolist()[0]}, {self.control_totals['GROUP_ID'].tolist()[-1]}]"

        # data view elements
        self.dv_imported_elements = self.get_dv_elements()
        self.dv_training_list = self.dv_imported_elements.query("USED_FOR_TRAINING == 'y'")['CATEGORY_NAME'].tolist()

    def get_dv_config(self):
        SQL = f"""
        select
            datasource = max(case when category_type = 'rawdatasource' then category_name end),
            dv_filter = max(case when category_type = 'filter' then category_name end),
            exp_defn = max(case when category_type = 'custom premium mode' then category_name end),
            EExp = max(case when category_type = 'custom expo field' then category_name end),
            EP = max(case when category_type = 'custom premium field' then category_name end),
            clm_defn = max(case when category_type = 'custom loss mode' then category_name end),
            CC = max(case when category_type = 'custom claim count field' then category_name end),
            IL = max(case when category_type = 'custom loss field' then category_name end),
            loss_cap = max(case when category_type = 'loss cap amount' then category_name end)
        from VIEW_DEFINITION 
        where view_id = '{self.dv_name}'
        """
        dv_config_dict = dict(pd.read_sql(SQL, self.conn).iloc[0])

        # some validations
        if dv_config_dict['dv_filter'] == '':
            print("handle missing dv_filter")
            dv_config_dict['dv_filter'] = '1=1'

        if dv_config_dict['CC'] == '':
            print("handle missing claim count")
            dv_config_dict['CC'] = '1'

        return dv_config_dict

    def get_dv_totals(self):
        pa_stats = PAStats(self.conn, self.config)
        return pa_stats._add_objectives(
            pa_stats.get_agg_totals(grouping_vars='GROUP_ID', analysis_id=None)
        )

    def get_dv_elements(self):
        SQL = f"""
        select CATEGORY_NAME, CATEGORY_TYPE, INFO_1, INFO_2, USED_FOR_TRAINING
        from VIEW_DEFINITION 
        where view_id = '{self.dv_name}' and category_type in ('ordinal', 'categorical', 'compound')
        """
        return pd.read_sql(SQL, self.conn)

    def find_data_elements_with_certain_keywords(self, kw_list):
        matching_cols = []
        for col in self.dv_imported_elements['CATEGORY_NAME'].tolist():
            for kw in kw_list:
                if kw.lower() in col.lower() and col not in matching_cols:
                    matching_cols.append(col)
        return self.dv_imported_elements[self.dv_imported_elements['CATEGORY_NAME'].isin(matching_cols)]
