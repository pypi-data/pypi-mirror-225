DB_SERVER = 'pa-va-sql02'
PLOTS_DIR_PATH = './tmp_plots'
INS_STATS_FORMATTING_DICT = {
    'EExp': '#,##0',
    'EP': '#,##0',
    'IL': '#,##0',
    'CC': '#,##0',
    'CC_pct': '0.00%',

    'Freq': '0.00',
    'Sev': '#,##0',
    'LC': '#,##0',
    'LR': '0.00%',

    'Freq_rel': '0.00',
    'Sev_rel': '0.00',
    'LC_rel': '0.00',
    'LR_rel': '0.00',

    'Loss': '#,##0',
    'Eval': '#,##0',
    'Avg_Loss': '#,##0',
    'Avg_Eval': '#,##0',
    'Ratio': '0.00%',
    'Avg_Loss_rel': '0.00',
    'Avg_Eval_rel': '0.00',
    'Ratio_rel': '0.00',

    'mean_loss': '#,##0',
    'mean_eval': '#,##0',
    'weighted_mean_ratios': '0.00%',
    'unweighted_mean_ratios': '0.00%',

    'mean_loss_rel': '0.00',
    'weighted_mean_ratios_rel': '0.00',
    'mean_eval_rel': '0.00',
    'weighted_mean_ratios_rel': '0.00',
    'unweighted_mean_ratios_rel': '0.00',

}

MAX_DISTINCT_CAT_VALUES_IF_UNBUCKETED = 30

def translate_rawscore_to_score(r, trans_df):
    return trans_df[trans_df['RAW_SCORE'] < (r + 0.000001)]['SCORE'].min()


def translate_rawscore_to_estimate(r, trans_df):
    return trans_df[trans_df['RAW_SCORE'] < (r + 0.000001)]['ESTIMATE_ALL'].max()

