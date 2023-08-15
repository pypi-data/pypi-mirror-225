import pandas as pd
from .config.config import API_COL_CONFIG_TABLE, API_COL_FIX_FCN, get_series_info


def overlap_with_specified_list(road_type_str, specified_list, overlap_text, no_overlap_text):
    if str(road_type_str) == 'nan':
        return None
    road_type_list = str(road_type_str).split(',') if str(road_type_str) != 'nan' else []
    if len(set(road_type_list).intersection(specified_list)) > 0:
        return overlap_text
    else:
        return no_overlap_text


def construction_uses_siding(const_str):
    if const_str is None:
        return False
    if "SIDING" in str(const_str).upper():
        return True
    else:
        return False


def construction_is_brick_stucco_concrete(wall_str):
    if wall_str is None:
        return False
    if "BRICK" in str(wall_str).upper():
        return True
    elif "STUCCO" in str(wall_str).upper():
        return True
    elif "CONCRETE" in str(wall_str).upper():
        return True
    else:
        return False


def construction_is_on_stilts_or_is_prefab(const_str):
    if const_str is None:
        return False
    if "STILT" in str(const_str).upper():
        return True
    elif "PREFAB" in str(const_str).upper():
        return True
    else:
        return False


class ApiBatch:
    def __init__(self, df, apply_data_fixes=True):
        self.df = df.copy()
        self.config = API_COL_CONFIG_TABLE

        self.match_info = self.summarize_match_stats()
        self.apply_data_fixes = apply_data_fixes
        if self.apply_data_fixes:
            print("apply data fixups")
            self.apply_column_fixups()
        self.batch_usage_summary_df = self.get_summary_usage()

    def summarize_match_stats(self):
        return {
            'location_type': self.df['location_type'].value_counts(dropna=False),
            'match_level': self.df['match_level'].value_counts(dropna=False),
            'match_scores': self.df.groupby('match_level')['match_score'].describe()
        }

    def apply_column_fixups(self):
        for col, fix_fcn in API_COL_FIX_FCN.items():
            if col in self.df.columns:
                if fix_fcn not in ['convert_feet_to_miles', 'parse_limited_access_and_dirt_roads', 'create_construction_features']:
                    self.df[col] = self.df[col].astype('str').apply(fix_fcn).astype('float')
                elif fix_fcn == 'convert_feet_to_miles':
                    # if value is "> 100" change value to 100... is the cap
                    idx_distance_gt100 = self.df[col] == '> 100'
                    self.df.loc[idx_distance_gt100, col] = 100

                    # convert values to float
                    self.df[col] = self.df[col].astype('float')

                    # if units are in feet, divide value by 5280 to convert to miles
                    if col == 'coast_distance.distance':  # shit... one example that breaks the pattern :(
                        unit_col_name = 'coast_distance.units'
                    else:
                        unit_col_name = col.replace('.value', '.units')
                    idx_uses_feet = self.df[unit_col_name] == 'feet'
                    self.df.loc[idx_uses_feet, col] = round(self.df.loc[idx_uses_feet, col] / 5280, 3)

                    # since I've converted all values to miles, update units accordingly
                    self.df[unit_col_name] = 'miles'

                elif fix_fcn == 'parse_limited_access_and_dirt_roads':
                    self.df["road_type_limited_access_ind"] = self.df[col].apply(
                        lambda x: overlap_with_specified_list(
                            x, specified_list=['DE', 'NO', 'OW'],  # dead-end, none, one-way
                            overlap_text="limited access (dead-end, one-way, None)",
                            no_overlap_text='')
                    )
                    self.df["road_type_dirt_road_ind"] = self.df[col].apply(
                        lambda x: overlap_with_specified_list(
                            x, specified_list=['AS', 'BR', 'CD', 'CO', 'PV'],
                            overlap_text="",
                            no_overlap_text='probable dirt road')
                    )

                elif fix_fcn == 'create_construction_features':
                    self.df["construction_uses_siding"] = self.df[['mls_listing_record_details.ex_exterior_wall_features', 'mls_listing_record_details.ex_construction_features']].apply(
                        lambda x: construction_uses_siding(x['mls_listing_record_details.ex_exterior_wall_features']) | construction_uses_siding(x['mls_listing_record_details.ex_construction_features']), axis=1
                    )
                    self.df["construction_is_brick_stucco_concrete"] = self.df[['mls_listing_record_details.ex_exterior_wall_features', 'mls_listing_record_details.ex_construction_features']].apply(
                        lambda x: construction_is_brick_stucco_concrete(x['mls_listing_record_details.ex_exterior_wall_features']) | construction_is_brick_stucco_concrete(x['mls_listing_record_details.ex_construction_features']), axis=1
                    )
                    # construction_is_on_stilts_or_is_prefab
                    self.df["construction_is_on_stilts_or_is_prefab"] = self.df[['mls_listing_record_details.ex_exterior_wall_features', 'mls_listing_record_details.ex_construction_features']].apply(
                        lambda x: construction_is_on_stilts_or_is_prefab(x['mls_listing_record_details.ex_exterior_wall_features']) | construction_is_on_stilts_or_is_prefab(x['mls_listing_record_details.ex_construction_features']), axis=1
                    )

        # drop all those stupid image columns
        images_cols = [col for col in self.df.columns if col.startswith("images")]
        self.df.drop(columns=images_cols, inplace=True)

    def get_summary_usage(self):
        # for the incoming dataframe, build a dataframe summarizing each column's usage pattern

        # generate summary values
        summary_info_dict = {}
        for col in self.df.columns.tolist():
            summary_info_dict[col] = get_series_info(self.df[col])
        summary_df = pd.DataFrame(data=summary_info_dict).T

        summary_df['data_type'] = self.df.dtypes.astype(str)
        summary_df = summary_df.reset_index().rename(columns={'index': 'column'})

        idx_is_batch_col = summary_df['column'].isin(self.config['column'])
        summary_df.loc[idx_is_batch_col, 'origin'] = 'HH_API'
        summary_df.loc[~idx_is_batch_col, 'origin'] = 'Client'

        summary_df = summary_df[['column', 'origin', 'data_type', 'distinct_val', 'missing_pct', 'concentration_pct']]
        return summary_df.merge(self.config, how='left', on='column').fillna('')

