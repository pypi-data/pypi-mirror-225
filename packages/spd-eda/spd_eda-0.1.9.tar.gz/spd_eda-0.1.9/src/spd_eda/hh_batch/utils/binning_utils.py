import pandas as pd


def apply_ntiles(s, num_ntiles):
    # determine domain values corresponding to desired percentiles... then use cut() instead of qcut() for consistency
    pctile_list = [pctiles / num_ntiles for pctiles in range(num_ntiles + 1)]
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_percentils(s, pctile_list):
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_fixed_cutpoints(s, fixed_cutpoints):
    if fixed_cutpoints[-1] == s.max():
        fixed_cutpoints[-1] = fixed_cutpoints[-1] + 0.01
    elif fixed_cutpoints[-1] < s.max():
        fixed_cutpoints.append(s.max() + 0.01)

    return pd.cut(s, bins=fixed_cutpoints, right=False, include_lowest=True, duplicates='drop')

# def _create_ordinal_bins(s, num_ntiles=None, pctil_list=None, fixed_cutpoints=None):
#     if num_ntiles:
#         return _apply_ntiles(s, num_ntiles)
#     elif pctil_list:
#         return _apply_percentils(s, pctil_list)
#     elif fixed_cutpoints:
#         return _apply_fixed_cutpoints(s, fixed_cutpoints)


def _convert_comma_separated_string_to_list(cs_string):
    return [float(val.strip()) for val in cs_string.split(',')]


def clean_default_bin_dict(def_dict):
    if def_dict['num_ntiles'] == '':
        def_dict['num_ntiles'] = None
    else:
        def_dict['num_ntiles'] = int(def_dict['num_ntiles'])

    if def_dict['pctile_list'] == '':
        def_dict['pctile_list'] = None
    else:
        def_dict['pctile_list'] = _convert_comma_separated_string_to_list(def_dict['pctile_list'])

    if def_dict['fixed_cutpoints'] == '':
        def_dict['fixed_cutpoints'] = None
    else:
        def_dict['fixed_cutpoints'] = _convert_comma_separated_string_to_list(def_dict['fixed_cutpoints'])

    return def_dict
