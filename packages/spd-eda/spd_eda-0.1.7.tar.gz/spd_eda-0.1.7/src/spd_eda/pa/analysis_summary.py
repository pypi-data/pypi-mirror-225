from .analysis import Analysis
from .config import INS_STATS_FORMATTING_DICT


class AnalysisSummary:  # TODO: return the analysis object so user can re-export easily to fix formatting shit
    def __init__(self, db_name, analysis_id,
                 geo_col='LOSSSTATE', naics_col='LOB',
                 objectives_to_format=[], stats_formatting=INS_STATS_FORMATTING_DICT
                 ):
        self.db_name = db_name
        self.analysis_id = analysis_id
        self.geo_col = geo_col
        self.naics_col = naics_col
        self.objectives_to_format = objectives_to_format  # TODO: default this to the analysis objective
        self.stats_formatting = stats_formatting

        # create analysis object
        self.analysis_obj = Analysis(self.db_name, self.analysis_id)
        self.analysis_obj._update_var_handling_dict(self.analysis_obj.sig_var_list)  # TODO: fire from Analysis?

        # update secondary variables TODO: possible to use Year instead?  Do they have to be part of DV?
        self.analysis_obj.update_geo_info(
            {'name': self.geo_col, 'ord_cat': 'cat', 'bin_strategy': 'dataview', 'bin_parameter': None}
        )
        self.analysis_obj.update_naics_info(
            {'name': self.naics_col, 'ord_cat': 'cat', 'bin_strategy': 'dataview', 'bin_parameter': None}
        )

        # process the features (Training variables only?  TODO: make this an option... all imported elements or trn)
        self.analysis_obj.process_features(self.analysis_obj.DV.dv_training_list, obj_fcn=self.objectives_to_format[0])

        # write the file  # TODO: some sort of confirmation message and/or return the analysis object
        self.analysis_obj.export_summary(f"ModelSummary_{self.analysis_id}.xlsx",
                                         obj_to_format=self.objectives_to_format,
                                         stats_formatting=INS_STATS_FORMATTING_DICT
                                         )
