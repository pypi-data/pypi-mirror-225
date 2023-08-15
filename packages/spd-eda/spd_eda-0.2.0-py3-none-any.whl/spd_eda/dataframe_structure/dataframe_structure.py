import pandas as pd


class DataframeStructure:
    def __init__(self, df):
        self.df = df
        self.shape = self.df.shape

    def thread_summary(self, thread):
        thread_summary_df = pd.DataFrame({
            'counts': self.df.groupby(thread).size().value_counts().sort_index()
        })
        thread_summary_df['pct'] = thread_summary_df['counts'] / thread_summary_df['counts'].sum()
        return thread_summary_df.reset_index().rename(columns={'index': 'rows_per_thread'})

    def thread_examples(self, thread, recs_per_thread, num_examples):
        counts_per_thread = self.df.groupby(thread, as_index=False).size()
        example_threads_df = counts_per_thread[counts_per_thread['size'] == recs_per_thread].iloc[:num_examples].drop(columns=['size'])
        return self.df.merge(example_threads_df, how='inner', on=thread).sort_values(thread)
