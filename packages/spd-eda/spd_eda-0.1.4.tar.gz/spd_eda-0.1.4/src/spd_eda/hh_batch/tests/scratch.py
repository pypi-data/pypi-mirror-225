from hh_batch import PortfolioAnalysis

print("start the analysis")
exception_cols = ['FormattedStreet', 'Formatted Risk City', 'Risk State (short)', 'zip_clean']
AL_obj = PortfolioAnalysis(
    analysis_name='PortfolioAnalysisSmokeTest',
    batch_filepath='spd_andover_sample_test2_parsed_part_1.csv',
    user_exception_column_list=exception_cols,
    max_records_per_exception=100
)
print("end the analysis")
