import pandas as pd


def apply_ntiles(s, num_ntiles):
    # determine domain values corresponding to desired percentiles... then use cut() instead of qcut() for consistency
    pctile_list = [pctiles / num_ntiles for pctiles in range(num_ntiles + 1)]
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_percentiles(s, pctile_list):
    cut_value_list = [s.quantile(pctile) for pctile in pctile_list]
    cut_value_list[-1] = cut_value_list[-1] + 0.01
    return pd.cut(s, bins=cut_value_list, right=False, include_lowest=True, duplicates='drop')


def apply_fixed_cutpoints(s, fixed_cutpoints):
    if fixed_cutpoints[-1] == s.max():
        fixed_cutpoints[-1] = fixed_cutpoints[-1] + 0.01
    elif fixed_cutpoints[-1] < s.max():
        fixed_cutpoints.append(s.max() + 0.01)

    return pd.cut(s, bins=fixed_cutpoints, right=False, include_lowest=True, duplicates='drop')


def apply_stand_alone_values(s, stand_alone_list, fallback_text="everything_else"):
    s2 = s.copy()
    in_stand_alone_idx = s2.isin(stand_alone_list)
    s2.loc[~in_stand_alone_idx] = fallback_text
    return s2


def return_binned_series(s, bin_info, fallback_text="everything_else"):
    bin_method, bin_param = bin_info
    if bin_method == 'num_ntiles':
        bin_s = apply_ntiles(s, bin_param)
    elif bin_method == 'pctile_list':
        bin_s = apply_percentiles(s, bin_param)
    elif bin_method == 'fixed_cutpoints':
        bin_s = apply_fixed_cutpoints(s, bin_param)
    elif bin_method == 'round':
        bin_s = s.round(bin_param)
    elif bin_method == 'cat_stand_alone_values':
        bin_s = apply_stand_alone_values(s, bin_param, fallback_text)
    else:
        bin_s = s
    return bin_s
