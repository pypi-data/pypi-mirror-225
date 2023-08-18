REFLECTION_ID_COLS = ['student_reflection_id_model', "student_user_id_model"]

import pandas as pd

def append_model_features(data_features, model_features):
    
    data_combined = data_features.copy(deep=False)
    for features in model_features:
        data_combined = pd.merge(data_combined,
                                 features.loc[:, features.columns.str.contains(
                                     '|'.join(["Top", "id"]))], on=REFLECTION_ID_COLS)

    return data_combined