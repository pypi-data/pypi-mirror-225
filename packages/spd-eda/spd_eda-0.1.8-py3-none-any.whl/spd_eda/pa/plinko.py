from .config import translate_rawscore_to_score, translate_rawscore_to_estimate
import pandas as pd


class Plinko:
    def __init__(self, model, policyno):
        self.model = model
        self.analysis_id = self.model.analysis_id
        self.policyno = policyno

        self.bmf = self.model._experiment_details.query("ELEMENT == 'Boosting Moderation Factor'").iloc[0]['VALUE']

        # query parameters
        self.source_table = model.DV.config['datasource']
        self.addl_filter = model.DV.config['exp_defn']

        # database queries
        self.Segments_df = self.get_segments_df()
        self.Iteration_Level_Response = self.get_iteration_level_response()
        self.Score_Trans_df = self.get_score_trans_df()

        # plinko trace
        self.plinko_df = self.plinko_it()

    def get_segments_df(self):
        sql = f"""
                select net_id, SUBINDEX, RULE_ID, FILTER, CLAIMS, PREMIUM, Objective
                from t_EE_SEGMENT_TOTALS
                where net_id = '{self.analysis_id}'
                """
        return pd.read_sql(sql, self.model.conn)

    def get_iteration_level_response(self):
        sql = f"""
                select SUBINDEX, iteration_lr = SUM(CLAIMS) / SUM(PREMIUM)
                from t_EE_SEGMENT_TOTALS
                where net_id = '{self.analysis_id}'
                group by SUBINDEX
                ORDER BY SUBINDEX
                """
        return pd.read_sql(sql, self.model.conn)

    def get_score_trans_df(self):
        sql = f"""
                select *
                from SCORING_TRANSFORMATION
                where analysis_id = '{self.analysis_id}'
                """
        return pd.read_sql(sql, self.model.conn)

    def plinko_it(self):
        Iter_Results = []
        for i in range(max(self.Segments_df['SUBINDEX']) + 1):
            This_Iteration_Segments = self.Segments_df[self.Segments_df['SUBINDEX'] == i]

            # 11/20/2019: GFB analyses have double apostrophes in the FILTER column... for example, (''FRAME'',''MV'')
            # I can't execute these snippetes, so will manually scrub those here
            Seg_list = ["when " + row.FILTER.replace("''", "'") + " then " + str(row.RULE_ID) for index, row in
                        This_Iteration_Segments.iterrows()]
            Seg_guts = '\n'.join(Seg_list)
            SQL = f"""
                select POLICYNO, SUBINDEX = {str(i)}, RULE_ID = CASE {Seg_guts} end
                from {self.source_table}
                where POLICYNO = '{self.policyno}' and {self.addl_filter}
                """
            Iter_Results.append(pd.read_sql(SQL, con=self.model.conn))
        Iterations = pd.concat(Iter_Results, ignore_index=True)

        # Join back to Segments_df to get FILTER and Objectives
        Iterations = pd.merge(Iterations, self.Segments_df[['SUBINDEX', 'RULE_ID', 'FILTER', 'Objective']],
                              on=['SUBINDEX', 'RULE_ID'])

        # Iteration Level Objective Values; the iteration-level objectives are all 1... check the arithmetic here
        Iterations = pd.merge(Iterations, self.Iteration_Level_Response, on=['SUBINDEX'])

        # get BMF.. should be 1.0 if boosting not used
        Iterations['BMF'] = float(self.bmf)

        # loop through and build the cumulative rawscore: (1) for iteration zero, 1.0 * (iteration_LR + BMF * (Objective - iteration_LR)); (2) subsequent iterations: prior_raw_score * (iteration_LR + BMF * (Objective - iteration_LR))
        Iterations['tmp_iter_adj'] = Iterations.apply(lambda x: x.iteration_lr + x.BMF * (x.Objective - x.iteration_lr),
                                                      axis=1)
        Iterations_cumprod = Iterations.groupby('POLICYNO')['tmp_iter_adj'].cumprod()
        Iterations['cumulative_rawscore'] = Iterations_cumprod

        # use SCORING_TRANSFORMATION to get score/estimates at each iteration
        Iterations['SCORE'] = Iterations.apply(
            lambda x: translate_rawscore_to_score(x.cumulative_rawscore, self.Score_Trans_df), axis=1)
        Iterations['ESTIMATE_ALL'] = Iterations.apply(
            lambda x: translate_rawscore_to_estimate(x.cumulative_rawscore, self.Score_Trans_df), axis=1)

        # grab the variable usage info from RULES_DATA
        rules = pd.read_sql(f"select * from rules_data where net_id = '{self.analysis_id}'", con=self.model.conn)
        all_in_one = rules.groupby(['SUBINDEX', 'RULE_ID', 'GROUP_ID'])['VALUE'].apply(
            lambda x: ', '.join(x.tolist())).unstack().fillna('').reset_index()
        Iterations = pd.merge(Iterations, all_in_one, on=['SUBINDEX', 'RULE_ID'])

        # reorder the significant variable columns
        SigVarList = self.model.sig_var_list  # ModelObject.SignificantVariables['group_id'].tolist()
        Pre_Var_list = Iterations.columns.tolist()[:-len(SigVarList)]
        Iterations = Iterations[Pre_Var_list + SigVarList]

        return Iterations
