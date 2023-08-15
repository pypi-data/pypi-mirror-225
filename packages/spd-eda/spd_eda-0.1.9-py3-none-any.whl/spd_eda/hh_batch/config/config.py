import os
import pandas as pd

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
API_COL_CONFIG_TABLE = pd.read_csv(os.path.join(DIR_PATH, "batch_column_config.csv"))
# ORD_BIN_CONFIG = pd.read_csv(os.path.join(DIR_PATH, "ordinal_bin_control_df.csv")).fillna('')
REPORT_TRANSLATION_TABLES = pd.read_excel(os.path.join(DIR_PATH, "report_translation_tables.xlsx"), sheet_name=None)
BATCH_DATA_DICTIONARY = pd.read_csv(os.path.join(DIR_PATH, "batch_data_dictionary.csv"))

###################################################
# for report configuration
###################################################


def convert_comma_string_to_list(c_str):
    if pd.isna(c_str):
        return []
    if c_str == '':
        return []
    else:
        return [x.strip() for x in c_str.split(',')]


def clean_report_config(df):
    df['column_list'] = df['column_list'].apply(convert_comma_string_to_list)
    df['bin_variables'] = df['bin_variables'].apply(convert_comma_string_to_list)
    for col in [col for col in df.columns if col.startswith("peril")]:
        # fun exception... has some different values
        if col != "peril_pl_cl":
            df[col] = df[col].apply(lambda x: True if x == 'X' else False)
    for col in [col for col in df.columns if col.startswith("use_case")]:
        df[col] = df[col].apply(lambda x: True if x == 'X' else False)
    if 'exclude_geo_errors' in df.columns.tolist():
        df['exclude_geo_errors'] = df['exclude_geo_errors'].apply(lambda x: True if x == 'X' else False)
    else:
        df['exclude_geo_errors'] = False

    return df


BASE_REPORT_CONFIG = clean_report_config(
    pd.read_csv(os.path.join(DIR_PATH, "base_report_config.csv"))
)

EXCLUDE_GEO_ERRORS_CONDITION = "status == 'ready'"

DEFAULT_EXCEPTION_COLS = [
    'state',
    'lat',
    'lng',
    'status',
    'location_type',
    'match_level',
    'match_score',
    'google_maps_url',
    'municipal_boundary.gid',
    'municipal_boundary.placefp',
    'municipal_boundary.namelsad',
    'municipal_boundary.type',
    'urbanicity.type',
    'urbanicity.name',
    'urbanicity.desc',
    'census_block.geoid',
    'census_block.state_fips_code',
    'census_block.county_fips_code',
    'census_block.tract',
    'census_block.block',
    'census_block.block_group',
    'state_county.state',
    'state_county.jurisdiction',
    'state_county.state_and_county_FIPS_code',
    'school_district.name',
    'tx_codes.com',
    'tx_codes.code',
    'tx_codes.county',
    'fl_codes.name',
    'property.owner',
    'property.use_code',
    'assessment.Air_Conditioning',
    'assessment.Air_Conditioning_Type',
    'assessment.Amenities',
    'assessment.Assessed_Improvement_Value',
    'assessment.Assessed_Land_Value',
    'assessment.Assessment_Year',
    'assessment.Basement',
    'assessment.Building_Area',
    'assessment.Building_Area_1',
    'assessment.Building_Condition',
    'assessment.Building_Quality',
    'assessment.Current_Owner_Name',
    'assessment.Fireplace',
    'assessment.Garage_Cars',
    'assessment.Garage_Type',
    'assessment.Heating',
    'assessment.LotSize_Acres',
    'assessment.LotSize_Depth_Feet',
    'assessment.LotSize_Frontage_Feet',
    'assessment.LSale_Price',
    'assessment.LSale_Recording_Date',
    'assessment.LValid_Price',
    'assessment.Main_Building_Area_Indicator',
    'assessment.No_of_Buildings',
    'assessment.No_of_Stories',
    'assessment.Number_of_Baths',
    'assessment.Number_of_Bedrooms',
    'assessment.Number_of_Partial_Baths',
    'assessment.Number_of_Units',
    'assessment.Owner1FirstName',
    'assessment.Owner1LastName',
    'assessment.Owner2Firstname',
    'assessment.Owner2LastName',
    'assessment.Owner_Occupied',
    'assessment.Pool',
    'assessment.PSale_Price',
    'assessment.Roof_Cover',
    'assessment.Roof_Type',
    'assessment.Standardized_Land_Use_Code',
    'assessment.Tax_Delinquent_Year',
    'assessment.tax_marketvalue',
    'assessment.Total_Assessed_Value',
    'assessment.Total_Market_Value',
    'assessment.Total_Number_of_Rooms',
    'assessment.Building_Class',
    'assessment.Type_Construction',
    'assessment.Year_Built',
    'mls_listing_record_details.ex_construction_features',
    'mls_listing_record_details.ex_exterior_wall_features',
    'mls_listing_record_details.ex_fence_features',
    'mls_listing_record_details.ex_foundation_features',
    'mls_listing_record_details.ex_garage_features',
    'mls_listing_record_details.ex_garage_spaces',
    'mls_listing_record_details.ex_general_features',
    'mls_listing_record_details.ex_lot_size_acres',
    'mls_listing_record_details.ex_lot_size_square_feet',
    'mls_listing_record_details.ex_lot_size_features',
    'mls_listing_record_details.ex_parking_features',
    'mls_listing_record_details.ex_parking_spaces',
    'mls_listing_record_details.ex_patio_features',
    'mls_listing_record_details.ex_patio_yn',
    'mls_listing_record_details.ex_pool_features',
    'mls_listing_record_details.ex_pool_yn',
    'mls_listing_record_details.ex_road_features',
    'mls_listing_record_details.ex_roof_features',
    'mls_listing_record_details.ex_sewer_features',
    'mls_listing_record_details.ex_spa_yn',
    'mls_listing_record_details.ex_style_features',
    'mls_listing_record_details.ex_view_features',
    'mls_listing_record_details.ex_wateraccess_features',
    'mls_listing_record_details.ex_waterfront_features',
    'mls_listing_record_details.if_appliance_features',
    'mls_listing_record_details.if_basement_features',
    'mls_listing_record_details.if_basement_yn',
    'mls_listing_record_details.if_cooling_features',
    'mls_listing_record_details.if_cooling_yn',
    'mls_listing_record_details.if_fireplace_features',
    'mls_listing_record_details.if_fireplace_number',
    'mls_listing_record_details.if_fireplace_yn',
    'mls_listing_record_details.if_floor_features',
    'mls_listing_record_details.if_general_features',
    'mls_listing_record_details.if_heating_features',
    'mls_listing_record_details.if_levels_features',
    'mls_listing_record_details.if_security_features',
    'mls_listing_record_details.if_security_system_yn',
    'mls_listing_record_details.if_utilities_features',
    'mls_listing_record_details.if_water_features',
    'mls_listing_record_details.if_window_features',
    'mls_listing_record_details.in_living_square_feet',
    'mls_listing_record_details.in_property_type',
    'mls_listing_record_details.in_public_remarks',
    'mls_listing_record_details.in_year_built',
    'mls_listing_record_details.in_association_features',
    'mls_listing_record_details.in_association_yn',
    'mls_listing_record_details.rm_baths_full',
    'mls_listing_record_details.rm_baths_half',
    'mls_listing_record_details.rm_baths_total',
    'mls_listing_record_details.rm_bedrooms_total',
    'mls_listing_record_details.rm_dining_features',
    'mls_listing_record_details.rm_family_yn',
    'mls_listing_record_details.rm_general_features',
    'mls_listing_record_details.rm_kitchen_features',
    'mls_listing_record_details.rm_laundry_features',
    'mls_listing_record_details.rm_rooms_total',
    'listing_record.list_date',
    'listing_record.list_price',
    'listing_record.status',
    'mortgage_info.Current_Est_LTV_Combined',
    'mortgage_info.Mtg01_Curr_Est_Bal',
    'mortgage_info.Mtg01_Loan_Amount',
    'mortgage_info.Mtg01_loan_type',
    'mortgage_info.Mtg01_Title_Company_Name',
    'mortgage_info.Total_Open_Lien_Balance',
    'valuation.price_range_max',
    'valuation.price_range_min'
    ]


###################################################
# Variable Summarization
###################################################

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


# For value transformations
def grab_numeric_part(s):
    # API output can be of the form, "<value> <Units>".  This functions strips the units and returns numeric value
    new_val = s.split(' ')[0]
    if len(new_val) > 0:
        try:
            return float(new_val)
        except ValueError:
            return None
    else:
        return None


def clean_no_stories(s):
    # API output for number of stories is really messy.  Limit to digits and period... and
    ok_chars = '0 1 2 3 4 5 6 7 8 9 .'.split(' ')
    clean_val = "".join([char for char in s if char in ok_chars])
    if len(clean_val) > 0:
        return float(clean_val)
    else:
        return None


def strip_pct(s):
    return float(str(s).replace('%', ''))


def clean_lstrikes_per_year_per_sqmile(s):
    # values of the form 95% chance of ### ground strikes in 1 year per square mile"
    return float(s.replace('95% chance of ', '').replace(' ground strikes in 1 year per square mile', ''))


def clean_lstrikes_per_year_10miles(s):
    # values of the form "### ground lightning strikes within 10 miles last year"
    return float(s.split(' ')[0])


def pull_numeric_from_first_position_null_guard(s):
    if len(str(s)) > 0:
        return float(str(s).split(' ')[0])
    else:
        return None


def get_high_range_of_indundation_levels(s):
    if s == "> 20 feet":
        return 25
    elif s == "< 1 foot":
        return 1
    elif "feet" in str(s):
        return int(str(s).split(' ')[-2])
    else:
        return None


def extract_radius_from_giant_wind_string(s):
    # example, grab 1.85 from "95% chance of damaging wind occurrence in 10 years in a 1.85 mile radius"
    if s is None:
        return None
    l_str = str(s).split(' ')
    if len(l_str) == 1:
        return None
    else:
        return float(l_str[11])


def extract_radius_from_giant_hail_tornado_string(s):
    # example, grab 1.88 from "95% chance of damaging hail occurrence in 10 years in 1.88 mile radius"
    # not a typo... wind message is "... in a ## radius", while hail is "... in ### radius" (no "a", lol)
    if s is None:
        return None
    l_str = str(s).split(' ')
    if len(l_str) == 1:
        return None
    else:
        return float(l_str[10])


API_COL_FIX_FCN = {
    'hh_elevation.aspect': grab_numeric_part,
    'aspect_risk.aspect': grab_numeric_part,
    'hh_elevation.elevation': grab_numeric_part,
    'hh_elevation.slope': grab_numeric_part,
    'slope_risk.slope': grab_numeric_part,
    'hospital.distance': grab_numeric_part,
    'urgent_care.distance': grab_numeric_part,
    'police_stations.distance': grab_numeric_part,

    'weather_params.annual_average_days_less_than_0': grab_numeric_part,
    'weather_params.annual_average_days_less_than_10': grab_numeric_part,
    'weather_params.annual_average_days_less_than_20': grab_numeric_part,
    'weather_params.annual_average_days_more_than_40': grab_numeric_part,
    'weather_params.annual_average_days_more_than_50': grab_numeric_part,
    'weather_params.annual_fall_days_less_than_0': grab_numeric_part,
    'weather_params.annual_fall_days_less_than_10': grab_numeric_part,
    'weather_params.annual_fall_days_less_than_20': grab_numeric_part,
    'weather_params.annual_fall_days_less_than_32': grab_numeric_part,
    'weather_params.annual_spring_days_less_than_0': grab_numeric_part,
    'weather_params.annual_spring_days_less_than_10': grab_numeric_part,
    'weather_params.annual_spring_days_less_than_20': grab_numeric_part,
    'weather_params.annual_spring_days_less_than_32': grab_numeric_part,
    'weather_params.annual_winter_days_less_than_0': grab_numeric_part,
    'weather_params.annual_winter_days_less_than_10': grab_numeric_part,
    'weather_params.annual_winter_days_less_than_20': grab_numeric_part,
    'weather_params.annual_winter_days_less_than_40': grab_numeric_part,
    'weather_params.average_annual_precipitation': grab_numeric_part,
    'weather_params.average_annual_snowfall': grab_numeric_part,
    'weather_params.average_annual_temperature_max': grab_numeric_part,
    'weather_params.average_annual_temperature_min': grab_numeric_part,
    'weather_params.average_days_snowfall_greater_than_10_inches': grab_numeric_part,
    'weather_params.average_days_snowfall_greater_than_1_inch': grab_numeric_part,
    'weather_params.average_fall_snowfall': grab_numeric_part,
    'weather_params.average_spring_snowfall': grab_numeric_part,
    'weather_params.average_winter_snowfall': grab_numeric_part,
    'weather_params.avg_days_snow_depth_above_10_in': grab_numeric_part,
    'weather_params.avg_days_snowfall_above_1_in': grab_numeric_part,
    'weather_params.avg_num_days_below_32_degrees': grab_numeric_part,
    'weather_params.avg_num_winter_days_below_32_degrees': grab_numeric_part,
    'weather_params.cooling_degree_days': grab_numeric_part,
    'weather_params.fall_days_snow_depth_greater_than_10_inches': grab_numeric_part,
    'weather_params.fall_days_snow_depth_greater_than_1_inch': grab_numeric_part,
    'weather_params.fall_days_snow_depth_greater_than_3_inches': grab_numeric_part,
    'weather_params.fall_days_snow_depth_greater_than_5_inches': grab_numeric_part,
    'weather_params.fall_diurnal_range': grab_numeric_part,
    'weather_params.fall_days_with_max_temp_less_than_32': grab_numeric_part,
    'weather_params.heating_degree_days': grab_numeric_part,
    'weather_params.spring_days_snow_depth_greater_than_10_inches': grab_numeric_part,
    'weather_params.spring_days_snow_depth_greater_than_1_inch': grab_numeric_part,
    'weather_params.spring_days_snow_depth_greater_than_3_inches': grab_numeric_part,
    'weather_params.spring_days_snow_depth_greater_than_5_inches': grab_numeric_part,
    'weather_params.spring_days_with_max_temp_less_than_32': grab_numeric_part,
    'weather_params.spring_diurnal_range': grab_numeric_part,
    'weather_params.winter_days_snow_depth_greater_than_10_inches': grab_numeric_part,
    'weather_params.winter_days_snow_depth_greater_than_1_inch': grab_numeric_part,
    'weather_params.winter_days_snow_depth_greater_than_3_inches': grab_numeric_part,
    'weather_params.winter_days_snow_depth_greater_than_5_inches': grab_numeric_part,
    'weather_params.winter_days_with_max_temp_less_than_32': grab_numeric_part,
    'weather_params.winter_diurnal_range': grab_numeric_part,

    'potential_maximum_precipitation': grab_numeric_part,
    'potential_catastrophic_precipitation': grab_numeric_part,

    'distance_to_significant_flood_params.distance_to_100yr_floodplain': pull_numeric_from_first_position_null_guard,
    'distance_to_significant_flood_params.elevation100': pull_numeric_from_first_position_null_guard,
    'distance_to_significant_flood_params.elevation_difference_100': pull_numeric_from_first_position_null_guard,

    'wind_born_debris.text': pull_numeric_from_first_position_null_guard,
    'wind_born_debris.year_2001.text': pull_numeric_from_first_position_null_guard,
    'wind_born_debris.year_2007.text': pull_numeric_from_first_position_null_guard,
    'wind_born_debris.year_2010.text': pull_numeric_from_first_position_null_guard,
    'wind_born_debris.year_2014.text': pull_numeric_from_first_position_null_guard,

    'surge_max.potential_inundation_level': get_high_range_of_indundation_levels,
    'surge_max.potential_inundation_level_4': get_high_range_of_indundation_levels,
    'surge_max.potential_inundation_level_3': get_high_range_of_indundation_levels,
    'surge_max.potential_inundation_level_2': get_high_range_of_indundation_levels,
    'surge_max.potential_inundation_level_1': get_high_range_of_indundation_levels,

    'assessment.No_of_Stories': clean_no_stories,

    'coast_distance.distance': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below
    'coast_distance.high_res_distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below
    'coast_distance.low_res_distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below
    'coast_distance.beach_distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below

    'nuclear_site_nearest.distance.value': 'convert_feet_to_miles',  #  not a univariate function... just apply as lambda below
    'toxic_release_facilities_params.distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below

    'clandestine_lab.distance': pull_numeric_from_first_position_null_guard,

    'enhanced_wind_params.wpctrisk': strip_pct,
    'enhanced_hail_params.hpctrisk': strip_pct,
    'enhanced_tornado_params.tpctrisk': strip_pct,
    'enhanced_lightning_params.lpctrisk': strip_pct,
    'enhanced_lightning_params.lsqmi': clean_lstrikes_per_year_per_sqmile,
    'enhanced_lightning_params.strikes_yr': clean_lstrikes_per_year_10miles,

    'drought_frequency_index.pct': strip_pct,
    'drought_frequency_index.desc': pull_numeric_from_first_position_null_guard,
    'pfa.text': pull_numeric_from_first_position_null_guard,
    'sinkhole.distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below
    'sinkhole_risk_params.sinkhole_distance.value': 'convert_feet_to_miles',  # not a univariate function... just apply as lambda below

    'enhanced_wind_params.historical_wind_events.wind_rad': extract_radius_from_giant_wind_string,
    'enhanced_hail_params.historical_hail_events.hail_rad': extract_radius_from_giant_hail_tornado_string,
    'enhanced_tornado_params.historical_tornado_events.tornado_rad': extract_radius_from_giant_hail_tornado_string,
    'ust_nearest_leaking.text': pull_numeric_from_first_position_null_guard,

    'mls_listing_record_details.ex_road_features': 'parse_limited_access_and_dirt_roads',
    'mls_listing_record_details.ex_construction_features': 'create_construction_features',

    'fault_earthquake.distance': pull_numeric_from_first_position_null_guard,
    'liquor_license.distance': pull_numeric_from_first_position_null_guard,
    'gun_dealers.distance': pull_numeric_from_first_position_null_guard,

}
