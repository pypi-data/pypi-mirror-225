from .config import DB_SERVER
from .connection import Connection

import pandas as pd
import xml.etree.ElementTree as ET


class DataSource:
    def __init__(self, db_name, ds_name, keyword_list):
        self.conn = Connection(DB_SERVER, db_name).str
        self.db_name = db_name
        self.ds_name = ds_name

        self.ds_all_column_list = self.get_all_ds_columns()

        self.ds_column_list = self.find_potential_tables(filter_cols=False)

        self.keyword_list = keyword_list
        self.potential_column_list = self.find_potential_tables(filter_cols=True)
        self.num_potential_columns = len(self.potential_column_list)

        self.ds_inheritance_list = self.find_ds_lineage()

    def get_all_ds_columns(self):
        SQL = f"select TABLE_NAME, COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where table_name = '{self.ds_name}'"
        return pd.read_sql(SQL, self.conn)['COLUMN_NAME'].to_list()

    def find_potential_tables(self, filter_cols):
        df_list = []
        if filter_cols:
            for keyword in self.keyword_list:
                SQL = f"select TABLE_CATALOG,TABLE_NAME, COLUMN_NAME from {self.db_name}.INFORMATION_SCHEMA.COLUMNS where table_name = '{self.ds_name}' and column_name like '%{keyword}%'"
                df_list.append(pd.read_sql(SQL, self.conn))
        else:
            SQL = f"select TABLE_CATALOG,TABLE_NAME, COLUMN_NAME from {self.db_name}.INFORMATION_SCHEMA.COLUMNS where table_name = '{self.ds_name}'"
            df_list.append(pd.read_sql(SQL, self.conn))
        if len(df_list) > 0:
            return pd.concat(df_list).drop_duplicates().reset_index(drop=True)['COLUMN_NAME'].tolist()
        else:
            return []

    def _if_land_data_grab_base_id(self, id):

        SQL = f"""
        select a.analysis_id, a.experiment_id, b.alg_type, b.base_analysis_id
        from analysis_details a
        left outer join (
        				select experiment_id,
        					alg_type = max(case when element = 'Algorithm Type' then value end),
        					base_analysis_id = max(case when element = 'Analysis' then value end)
        				From EXPERIMENT_DETAILS
        				group by experiment_id
        				) b on a.EXPERIMENT_ID = b.EXPERIMENT_ID
        where a.analysis_id = '{id}'
        """
        land_data_info_df = pd.read_sql(SQL, self.conn)
        if land_data_info_df.shape[0] == 0:
            return id
        if land_data_info_df.iloc[0]['base_analysis_id']:
            return land_data_info_df.iloc[0]['base_analysis_id']
        else:
            return id

    def _grab_unmangled_analysis_id(self, mangled_id):
        if mangled_id:
            frag_id = "-".join(mangled_id.split('-')[-4:])
            potential_matches = pd.read_sql(f"select * from analysis_details where analysis_id like '%{frag_id}%'",
                                            self.conn)
            if potential_matches.shape[0] == 1:
                return potential_matches.iloc[0]['ANALYSIS_ID']

    def _extract_xml_info(self, xml_info):
        root = ET.fromstring(xml_info)
        new_columns = root.findall('column')
        inherited_cols = []
        for idx, column in enumerate(new_columns):
            inherited_col_name = column.find('name').text
            parent_analysis_id = column.find('base_analysis').find('analysis_id').text
            parent_analysis_id_clean = self._grab_unmangled_analysis_id(parent_analysis_id)
            # check if this is land data... if so, grab base ID
            parent_analysis_id_clean = self._if_land_data_grab_base_id(parent_analysis_id_clean)

            parent_analysis_type = column.find('base_analysis').find('type').text
            parent_analysis_objective = column.find('base_analysis').find('goal').text

            inherited_cols.append((inherited_col_name, parent_analysis_id, parent_analysis_id_clean,
                                   parent_analysis_type, parent_analysis_objective))
        return inherited_cols

    def _find_parent_ds_info(self, child_ds_name):
        parent_ds_info = pd.read_sql(f"select * from CUSTOM_DATASET where Name = '{child_ds_name}'", self.conn)
        if parent_ds_info.shape[0] == 1:
            parent_ds_name = parent_ds_info.iloc[0]['BaseDatasetName']
            parent_payload_xml = parent_ds_info.iloc[0]['ColumnsXML'].replace('\t', '').replace('\r', '').replace('\n',
                                                                                                                  '').replace(
                ' ', '')
            return (parent_ds_name, self._extract_xml_info(parent_payload_xml))

    def find_ds_lineage(self):
        lineage = []
        child_ds = self.ds_name
        while self._find_parent_ds_info(child_ds):
            parent_ds, inheritance_info = self._find_parent_ds_info(child_ds)
            lineage.append((parent_ds, inheritance_info))
            child_ds = parent_ds
        return lineage

    def find_ds_columns_with_certain_keywords(self, kw_list):
        matching_cols = []
        for col in self.ds_all_column_list:
            for kw in kw_list:
                if kw.lower() in col.lower() and col not in matching_cols:
                    matching_cols.append(col)
        return matching_cols

    def get_col_distn(self, col_name):
        SQL = f"select {col_name}, count(1) as 'n' from {self.ds_name} group by {col_name} order by 'n' desc"
        df = pd.read_sql(SQL, self.conn)
        df['pct'] = df['n'] / df['n'].sum()
        return df

