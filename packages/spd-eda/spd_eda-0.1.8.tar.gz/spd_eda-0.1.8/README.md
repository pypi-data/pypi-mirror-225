
# SPD's collection of EDA tools

## For use on pandas dataframes

### `DataFrameEDA`
Use the `DataFrameEda` class for quick analysis on a pandas dataframe.

```
from spd_eda import DataframeEda

DataframeEda(
    df, agg_fcn,
    control_var_list=[], ord_bin_threshold=100, ord_bin_count=5, cat_value_limit=30
    )
```
Arguments:
- `df`: dataframe to be reviewed
- `ag_fcn`: user-defined aggregation function that can be applied to the dataframe
- `control_var_list` (optional): list of additional one-way variables for control totals (defaults to empty list)
- `ord_bin_threshold` (optional): maximum number of distinct numeric values before bucketing will occur (default=100)
- `ord_bin_count` (optional): If ordinal bucketing occurs, determines number of `pd.cut()` buckets (default=5)
- `cat_value_limit` (optional): maximum number of distinct categorical values before bucketing will occur (default=30)
- `calculate_signals` (optional): boolean for whether to calculate signals (based on agg_fcn) for each variable
- `signal_weight_col` (optional): if signals are calculated, this is the column to use for weighting.  If omitted, will use the first column from the agg_fcn
- `calculate_cramers_v` (optional): boolean for whether to calculate cramers V against each of the control variables (from `control_var_list`)
- `start_with_user_provided_summary_df` (optional): boolean to specify if user will provide the summary dataframe.  If False, will use pd.describe()
- `user_provided_summary_df` (optional): if user providing summary dataframe, column names MUST be in the index.

### `ExcelExport`
Use the `ExcelExport` class to write results of the `DataFrameEda` into excel.

```
from spd_eda import ExcelExport

ExcelExport(
    filename, control_df_list, col_summary_df, var_info_dict,
    col_type_dict={}, col_cond_format_list=[]
    )
```
Arguments:
- `filename`: name of excel file to be created (e.g. 'sample_output.xlsx')
- `control_df_list`: a list of dataframes to include on the 'control' tab of the output
- `col_summary_df`: single dataframe with one record per column... first column should be the variable name
- `var_info_dict`: dictionary where keys are column names & values are one-way stats for the variable (using the agg function)
- `col_type_dict` (optional): dictionary to control number formatting in excel
- `col_cond_format_list` (optional): list of columns to conditionally format in the excel


Sample usage:

```
from spd_eda import DataframeEda, ExcelExport

# define an aggregation function
def my_agg_fcn(df):
    return df.agg({'fid': 'count', 'building_a': 'mean',})

# create EDA object
eda_obj = DataframeEda(df, my_agg_fcn, control_var_list=['city'])

# formatting options
col_type_dict = {
        'fid': '#,##0',
        'building_a': '#,##0',
        }
col_cond_format_list = ['fid']

# export it
ExcelExport('EDA_station_16_addresses.xlsx',
            eda_obj.control_df_list, eda_obj.var_summary, eda_obj.var_info_dict,
            col_type_dict=col_type_dict, col_cond_format_list=col_cond_format_list)
```

## For use on PA/Predict entities

Must be running from a machine with database access.


### `DataViewEda` 
The `DataViewEda` class for doing quick analysis on a data view in the Predict software.

```
DataViewEda(
    db_name, dv_name,
    secondary_var_list=[], bin_override_dict={}
    )
```

Arguments:
- `db_name`: database name
- `dv_name`: data view name
- `secondary_var_list` (optional): list of secondary fields that be part of two-way comparisons for all data elements
- `bin_override_dict` (optional): dictionary of binning overrides (default={})

Once object is instantiated, use the `export_summary()` method to create formatted output in excel.

```
export_summary(
    filename, obj_to_format,
    stats_formatting=INS_STATS_FORMATTING_DICT
    )
```
Arguments:
- `filename`: name of excel file to be created (e.g. 'dv_summary.xlsx')
- `obj_to_format`: list of columns to conditionally format (e.g. ['EExp', 'LR'])
- `stats_formatting` (optional): dictionary of column formats for the output.  Has sensible defaults already, but format is like this: {'Freq': '0.00', 'Sev': '#,##0', 'LR': '0.00%'}


Sample usage:

```
from spd_eda import DataViewEda

test_dv_eda = DataViewEda(
        'GuidewireResearchCM_Insight',
        'eda_testing',
        secondary_var_list=['ax_year', 'LOSSSTATE'],
        )

test_dv_eda.export_summary("DataViewEDA_eda_testing.xlsx", obj_to_format=['LR'])       
```


### `AnalysisSummary` 
The `AnalysisSummary` class supplements the analysis that comes from the Predict software, producing a file of the form `ModelSummary_<analysis_id>.xlsx`.

```
AnalysisSummary(
    db_name, analysis_id,
    geo_col='LOSSSTATE', naics_col='LOB',
    objectives_to_format=[], stats_formatting=INS_STATS_FORMATTING_DICT
    )
```
Arguments:
- `db_name`: database name
- `analysis_id`: analysis ID
- `geo_col`: column name <b> already included in the data view</b> to use for geography (will be used in two-way exhibits)
- `naics_col`: column name <b> already included in the data view</b> to use for naics (can be anything... will just be used for two-ways)
- `objectives_to_format` (optional): list of columns to conditionally format (e.g. ['EExp', 'LR'])
- `stats_formatting` (optional): dictionary of column formats for the output.  Has sensible defaults already, but format is like this: {'Freq': '0.00', 'Sev': '#,##0', 'LR': '0.00%'}


Sample usage:

```
from spd_eda import AnalysisSummary

AnalysisSummary(
    db_name='GuidewireCooperativeModelsClaimsHO_Insight',
    analysis_id='711b0a41-a49b-46df-8dff-68dd04776520',
    geo_col='LOSSSTATE', naics_col='LOB', objectives_to_format=['Freq']
    )      
```



### `Plinko` 
The `Plinko` class can be used to trace an individual policy through a Boosting model from Predict.

Note that the `Plinko` model references the `Analysis` class, which is briefly defined below. 

```
Analysis(db_name, analysis_id)
```
Arguments:
- `db_name`: database name
- `analysis_id`: analysis ID


```
Plinko(model, policyno)
```
Arguments:
- `model`: an `Analysis` object corresponding to a Boosting model
- `policyno`: a specific POLICYNO value from the original modeling dataset (i.e. needs the model variable for the model)

Properties:
- `plinko_df`: dataframe that traces the specific example through all the iterations of the boosting model


Sample usage:

```
from spd_eda import Analysis, Plinko

# create Analysis object
model = Analysis(
    db_name='GuidewireCooperativeModelsClaimsHO_Insight',
    analysis_id='711b0a41-a49b-46df-8dff-68dd04776520'
    )

# create specific plinko object
plinko_obj = Plinko(model, '63_155334')

# review the trace file
plinko_obj.plinko_df      
```



## For use on Athena tables

Must have appropriate AWS credentials to connect.


### `AthenaTable`
Use the `AthenaTable` class for doing quick analysis on tables in AWS Athena

```
AthenaTable(db_name, tbl_name)
```
Arguments:
- `db_name`: database name
- `tbl_name`: table name


Available properties:

- `row_count`: integer value with number of rows in the table
- `information_schema`: dataframe with metadata on the columns in the table
- `col_info`: dictionary of key: value pairs, where key is the column name & value is dataframe of (binned) record counts

Available methods:

- `get_sample_records(num_rows=10, filter_string="1=1", col_subset_list=[])` - returns dataframe
- `get_row_count(filter_string="1=1")` - returns row count, note the optional filter
- `get_custom_counts(custom_expression)` - returns record counts based on the provided expression
- `get_records_per_thread_summary(thread_list, filter_string="1=1")` - Define a "thread" as set of columns, provides value distribution of # records that exist within each thread (useful for finding keys)
- `get_thread_examples_with_specified_num_records(thread_list, records_per_thread, num_thread_examples=1, filter_string="1=1")` - returns dataframe with examples of "threads" with the desired number of "records-per-thread".  Useful in conjunction with `get_records_per_thread_summary()`
- `get_column_info()` - This populates the `col_info` attribute... can take a long time to run.
- `write_summary(filename)` - creates excel file summarizing the table

Sample Usage:
```
from spd_eda import AthenaTable

EDA_osha_accident_injury_raw = AthenaTable('assess_db', 'osha_accident_injury_raw')

# distributions by column & expression
EDA_osha_accident_injury_raw.get_custom_counts("degree_of_inj")
EDA_osha_accident_injury_raw.get_custom_counts("SUBSTRING (load_dt, 1, 4)")

# thread hunting
EDA_osha_accident_injury_raw.get_records_per_thread_summary(['summary_nr'])
EDA_osha_accident_injury_raw.get_records_per_thread_summary(['summary_nr', 'injury_line_nr'])
EDA_osha_accident_injury_raw.get_thread_examples_with_specified_num_records(['summary_nr', 'injury_line_nr'], 2, num_thread_examples=3)

# generating excel summary
EDA_osha_accident_injury_raw.get_column_info()
EDA_osha_accident_injury_raw.write_summary('EDA_osha_accident_injury_raw.xlsx')
```

