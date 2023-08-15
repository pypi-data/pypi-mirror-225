import pandas as pd
from .utils.excel_utils import default_report_sheet
from .utils.stat_utils import default_agg_fcn
from .utils.binning_utils import apply_ntiles, apply_percentils, apply_fixed_cutpoints
from .config.config import REPORT_TRANSLATION_TABLES, BATCH_DATA_DICTIONARY


geocoding_exceptions = {
    'geocoding_error': "status == 'geocoding_error'",
    'non_house_match': "match_level != 'houseNumber'",
    'poor_house_match': "(match_level == 'houseNumber') & (match_score < 0.7)"
}

hurricane_history_exceptions = {
    'num_disturbances_gt0': "(`enhanced_hurricane_params.num_disturbances` > 0)",
    'num_cat2_gt0': "(`enhanced_hurricane_params.num_cat_2_hurricanes` > 0)",
    'num_cat3_gt0': "(`enhanced_hurricane_params.num_cat_3_hurricanes` > 0)",
    'num_cat4_gt0': "(`enhanced_hurricane_params.num_cat_4_hurricanes` > 0)",
    'num_cat5_gt0': "(`enhanced_hurricane_params.num_cat_5_hurricanes` > 0)",

}

wind_debris_exceptions = {
    'wind_debris_overall': "(`wind_born_debris.score` in ('D', 'F'))",
    'wind_debris_2001': "(`wind_born_debris.year_2001.score` in ('D', 'F'))",
    'wind_debris_2007': "(`wind_born_debris.year_2007.score` in ('D', 'F'))",
    'wind_debris_2010': "(`wind_born_debris.year_2010.score` in ('D', 'F'))",
    'wind_debris_2014': "(`wind_born_debris.year_2014.score` in ('D', 'F'))",

}

land_use_exception_condition_for_filter = "'Boat slips, Marina, Yacht Club (recreation/pleasure), Boat Landing', 'Commercial-Vacant Land', 'Forest (park; reserve; recreation, conservation)', 'Homes (retired; handicap, rest; convalescent; nursing)', 'Nightclub (Cocktail Lounge)', 'Vacant Land (General)'"

mls_road_exceptions = {
    'limited_access': "(road_type_limited_access_ind == 'Yes')",
    'probable_dirt_road': "(road_type_dirt_road_ind == 'probable dirt road')",
}

mls_construction_exceptions = {
    'siding_on_non_sturdy_bldg': "(construction_uses_siding == True) & (construction_is_brick_stucco_concrete == False)",
    'on_stilts_or_prefab_construction': "(construction_is_on_stilts_or_is_prefab == True)",
}

REPORT_EXCEPTIONS = {
    'geocoding': geocoding_exceptions,
    'wildfire_perimeters': {'named_perimeter': "(`enhanced_wildfire.wildfire_perimeter_risk.proximate_wildfire_perimeters.0.name` > '')"},
    'perennial_water': {'nearby_water_source': "(`perennial_water.name` > '')"},
    'fault_earthquake': {'nearby_earthquake': "(`fault_earthquake.name` > '')"},
    'fracking': {'nearby_fracking_earthquake': "(`fracking_earthquake.score` > '')"},
    'designated_fault': {'in_usgs_eastern_fault_zone': "(`designated_fault.score` == 'C')"},
    'mudslide': {'mudslide_risk': "(`mudslide_risk.PCL` > '')"},
    'lava_flow': {'lava_risk': "(`lava_flow.text` > '')"},
    'tsunami': {'tsunami_score': "(`tsunami.score` == 'C')"},
    'hurricane_history': hurricane_history_exceptions,
    'superfund': {'near_superfund_site': "(`superfund.score` in ('C', 'D'))"},
    'brownfield': {'near_brownfield_site': "(`brownfield.score` in ('C', 'D'))"},
    'pfa': {'near_pfa_site': "(`pfa.score` in ('C', 'D'))"},
    'sinkhole': {'sinkhole_within_1000_ft': "(`sinkhole.score` in ('C', 'D'))"},
    'sinkhole_rings': {"sinkhole_within_1_mile": "(`sinkhole_ring_params.cummulative_0_1_mile` > 0)"},
    'wind_radius': None,  # TODO fix up the wind_rad value & then get values less than 1.5 miles
    # TODO confirm these adjustments fo flood exceptions... adding the D/F conditions
    'flood_score': {'nearby_flood_line': "(`enhanced_hazardhub_flood.score` in ('D', 'F')) & (`enhanced_hazardhub_flood_params.lines_name` > '')"},
    'flood_params': {'nearby_flood_polygon': "(`enhanced_hazardhub_flood_params.polygons_score` in ('D', 'F')) & (`enhanced_hazardhub_flood_params.polygon_name` > '')"},
    'fema_sfha': {'in_special_flood_haz_area': "(`fema_all_flood_params.sfha_tf` == 'T')"},
    # TODO: what's the exception condition for elevation?
    # TODO: what's the exception condition for a slope?
    'wind_pool': {'near_wind_pool': "(`wind_pool.score` in ('D', 'F'))"},
    'wind_debris': wind_debris_exceptions,
    'mine_subsidence': {'near_mine_subsidence': "(`mine_subsidence.score` in ('C', 'D'))"},
    # TODO: add surgemax
    # TODO: add coast distance exception (after confirming I've handled underlying values correctly)
    # TODO: add sea level rise condition
    'hu_reins_tier': {'in_reinsurance_tier': "(`re_tier_counties.value` in ('1', '2', 1, 2))"},
    # add tammy's suggestions
    'fs1_drive_mins': {'15+_mins_away': "(`drive_time_fire_station.duration` >= 15)"},
    'fs_density10': {'LT2_in_10_miles': "(`number_of_fire_stations_within_10_miles` < 2)"},
    'assessment_land_use_code': {'exception_codes': f"(`assessment.Standardized_Land_Use_Code` in ({land_use_exception_condition_for_filter}))"},
    'fema_flood_distances': {'lower_than_floodzone_and_within100_ft': "(`distance_to_significant_flood_params.distance_to_100yr_floodplain` < 100) & (`distance_to_significant_flood_params.elevation_difference_100` < 0)"},

    # 'mls_road': mls_road_exceptions,
    # 'mls_construction': mls_construction_exceptions

}


# fixed_cutpoints, pctile_list, num_ntiles
ORD_BIN_INFO = {
    'match_score': ('fixed_cutpoints', [0, 0.5, 0.7, 0.8, 0.9, 1]),
    'nearest_fire_station.distance': ('round', 0),
    'drive_distance_fire_station.distance': ('round', 0),
    'nearest_fire_station_2.distance': ('round', 0),
    'nearest_fire_station_2.drive_distance_fire_station.distance': ('round', 0),
    'nearest_fire_station_3.distance': ('round', 0),
    'nearest_fire_station_3.drive_distance_fire_station.distance': ('round', 0),
    'soil_shear_velocity.vs30':  ('pctile_list', [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1]),
    'enhanced_hurricane_params.avg_wind_speed_knots': ('round', 0),
    # tammy's suggestions
    'enhanced_hurricane_params.scale': ('round', 0),  # TODO: add to config bin columns :(
    'sinkhole.distance.value': ('round', 2),
    'enhanced_wind_params.historical_wind_events.wind_rad': ('round', 1),
    'enhanced_wind_params.waddrisk':  ('round', 2),
    'enhanced_wind_params.wpctrisk': ('round', 2),
    'enhanced_hail_params.historical_hail_events.hail_rad': ('round', 1),
    'enhanced_tornado_params.historical_tornado_events.tornado_rad': ('round', 1),
    'mold_index.index': ('round', 0),
    'coast_distance.distance': ('round', 3),
    'coast_distance.high_res_distance.value': ('round', 3),
    'coast_distance.low_res_distance.value': ('round', 3),
    'coast_distance.beach_distance.value': ('round', 3),

}


# For variable summaries
def get_series_info(s):
    # For a Series, summarize some usage values: number of distinct values, pct of missing values and concentration pct
    info_dict = {
        'distinct_val': s.nunique(),
        'missing_pct': pd.isna(s).sum() / s.shape[0],
        'concentration_pct': s.value_counts(dropna=False).iloc[0] / s.shape[0]
    }
    s_info = pd.Series(info_dict)
    s_info.name = s.name
    return s_info


class Report:
    def __init__(self, report_name, df, worksheet_fcn=None,
                 agg_fcn=None, agg_fcn_input_list=None,
                 bin_cols=None, custom_bin_dict=None,
                 report_trans_dict=None, batch_data_dictionary=None,
                 exception_dict=None, user_exception_column_list=None, max_records_per_exception=None,
                 ):
        self.report_name = report_name
        self.df = df.copy()

        self.worksheet_fcn = worksheet_fcn if worksheet_fcn else default_report_sheet
        self.agg_fcn = agg_fcn if agg_fcn else default_agg_fcn
        self.agg_fcn_input_list = [] if agg_fcn_input_list is None else agg_fcn_input_list
        self.bin_cols = bin_cols if bin_cols else []
        self.custom_bin_dict = custom_bin_dict
        self.report_trans_dict = REPORT_TRANSLATION_TABLES if report_trans_dict is None else report_trans_dict
        self.batch_data_dictionary = BATCH_DATA_DICTIONARY if batch_data_dictionary is None else batch_data_dictionary
        self.exception_dict = exception_dict if exception_dict else REPORT_EXCEPTIONS.get(self.report_name, {})
        self.user_exception_column_list = [] if user_exception_column_list is None else user_exception_column_list
        self.max_records_per_exception = max_records_per_exception

        self.cols_to_analyze = [col for col in self.df.columns.tolist() if col not in self.user_exception_column_list and col not in self.agg_fcn_input_list]

        # binning related
        self.bin_info = self.determine_binning_dictionary()
        self.bin_df = self.apply_binning()

        # populate exhibits
        print(f"start generating exhibits for {self.report_name}")
        self.exhibits_dict = self.generate_exhibits()

    def determine_binning_dictionary(self):
        if self.custom_bin_dict is None:
            return {var: bin_info for (var, bin_info) in ORD_BIN_INFO.items() if var in self.bin_cols}
        else:
            return {var: bin_info for (var, bin_info) in self.custom_bin_dict.items() if var in self.bin_cols}

    def return_binned_series(self, col, bin_info):
        bin_method, bin_param = bin_info
        if bin_method == 'num_ntiles':
            bin_s = apply_ntiles(self.df[col], bin_param)
        elif bin_method == 'pctile_list':
            bin_s = apply_percentils(self.df[col], bin_param)
        elif bin_method == 'fixed_cutpoints':
            bin_s = apply_fixed_cutpoints(self.df[col], bin_param)
        elif bin_method == 'round':
            bin_s = self.df[col].round(bin_param)
        else:
            bin_s = self.df[col]
        return bin_s

    def apply_binning(self):
        bin_df = self.df.copy()
        orig_col_order = self.df.columns.tolist() # self.cols_to_analyze
        for var, bin_info in self.bin_info.items():
            bin_series = self.return_binned_series(var, bin_info)
            other_cols = [col for col in orig_col_order if col != var]
            bin_df = pd.concat([bin_df[other_cols], bin_series], axis=1).copy()  # [orig_col_order].copy()
        return bin_df[orig_col_order]

    def summarize_column_usage(self):
        # generate summary values
        summary_info_dict = {}
        for col in self.cols_to_analyze:
            summary_info_dict[col] = get_series_info(self.df[col])
        summary_df = pd.DataFrame(data=summary_info_dict).T
        summary_df = summary_df.reset_index().rename(columns={'index': 'column'})

        return summary_df[['column', 'distinct_val', 'missing_pct', 'concentration_pct']]

    def _get_exception_records(self, rule_nm, rule_defn):
        exception_df = self.df.query(rule_defn)
        exception_df['condition'] = rule_nm
        col_order = ['condition'] + self.user_exception_column_list + self.cols_to_analyze
        return exception_df[col_order]

    def summarize_exception_conditions(self):
        # exceptions MUST be against the raw data... no binning applied
        if self.exception_dict:
            exception_names = []
            exception_rules = []
            exception_counts = []
            exception_examples = []
            for rule_nm, rule_defn in self.exception_dict.items():
                exception_names.append(rule_nm)
                exception_rules.append(rule_defn)
                try:
                    exception_df = self._get_exception_records(rule_nm, rule_defn)
                    num_exceptions = exception_df.shape[0]
                    exception_counts.append(num_exceptions)
                    if self.max_records_per_exception and self.max_records_per_exception < num_exceptions:
                        exception_examples.append(exception_df.iloc[:self.max_records_per_exception])
                    else:
                        exception_examples.append(exception_df)

                except TypeError:
                    print(f"******  data type error processing rule {rule_nm} ****************")
                    exception_counts.append(0)

            exception_summary = pd.DataFrame({
                'condition': exception_names,
                'num_exceptions': exception_counts,
                'rule_logic': exception_rules
            })
            if len(exception_examples) > 0:
                exception_examples = pd.concat(exception_examples)
            else:
                exception_examples = pd.DataFrame([])
            return {'summary': exception_summary, 'examples': exception_examples}
        else:
            return {'summary': pd.DataFrame([]), 'examples': pd.DataFrame([])}

    def summarize_applicable_documentation(self):
        doc_df = self.batch_data_dictionary.copy()
        doc_df = doc_df[doc_df['column'].isin(self.cols_to_analyze)]
        if doc_df.shape[0] > 0:
            return doc_df
        else:
            return pd.DataFrame([])

    def generate_exhibits(self):
        exception_info_dict = self.summarize_exception_conditions()
        return {
            'usage_summary': self.summarize_column_usage(),
            'one_way_stats': self.bin_df.groupby(self.cols_to_analyze, dropna=False, as_index=False).apply(
                self.agg_fcn),
            'exception_summary': exception_info_dict['summary'],
            'exception_examples': exception_info_dict['examples'],
            'metadata': self.report_trans_dict.get(self.report_name, pd.DataFrame([])),
            'dictionary': self.summarize_applicable_documentation()

        }

    def write_report_sheet(self, writer):
        if self.worksheet_fcn is None:
            return default_report_sheet(writer, self.report_name, self.exhibits_dict)
        else:
            return self.worksheet_fcn(writer, self.report_name, self.exhibits_dict)
