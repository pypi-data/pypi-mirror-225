import pickle
import os
import joblib
import pandas as pd
import numpy as np
from imblearn.combine import SMOTEENN

CLASSES = [0, 1, 2, 3, 4]

def resample_train_data(x_train, y_train):
    smote_enn = SMOTEENN(random_state=0)
    x_resampled, y_resampled = smote_enn.fit_resample(x_train, y_train)
    x_train = pd.DataFrame(data=x_resampled, columns=x_train.columns)
    y_train = y_resampled

    return x_train, y_train


def drop_id_cols(data):
    data = data.loc[:, ~data.columns.duplicated()]
    cols = [c for c in mod.REFLECTION_ID_COLS if c in data.columns]
    data_id = data[cols]
    data_train = data.drop(cols, axis=1)

    return {"dataid": data_id, "data": data_train}


def append_columns(data1, data2):
    return pd.concat([data1.copy(deep=False).reset_index(drop=True),
                      data2.copy(deep=False).reset_index(drop=True)], axis=1)


def get_model_object(modelname):
    return joblib.load(modelname) if isinstance(modelname, str) else modelname


def get_xgb_features(data):
    file_name = f"{mod.PROD_MODEL_PATH_1}/features_xgb_model"
    with open(file_name, 'rb') as file:
        features_xgb_model = pickle.load(file)

    return data[features_xgb_model]


def get_top1_top2(modelname, results):
    results[modelname + "_Pred_Top_1"] = get_tops(results, 1, CLASSES)
    results[modelname + "_Pred_Top_2"] = get_tops(results, 2, CLASSES)

    results.columns = [f"{modelname}_Prob_{c}"
                       if c in CLASSES else c
                       for c in results.columns]
    results.rename(columns={'abs_predictions': f"{modelname}_abs_predictions"}, inplace=True)

    return results


def get_tops(data, rank, classes):
    return pd.to_numeric(data[classes].
                         columns[data[classes].
                                 values.argsort(1)[:, -rank]])


def create_feature_list(features, score, dataid):
    return {"features": features,
            "score": score,
            "dataid": dataid}


def create_model_features(agg_data_train, pred_functions):
    return [pred_function(agg_data_train.copy(deep=False))
            for pred_function in pred_functions]


def create_training_data(agg_data_train):
    data_x = agg_data_train.copy(deep=False).drop("score_model", axis=1)
    data_y = append_columns(data_x[REFLECTION_ID_COLS], agg_data_train.score_model)
    return data_x, data_y


def get_score(score):
    return np.array(drop_id_cols(score)["data"].values.ravel(), dtype=np.int8)


def get_object_name(pathname):
    return os.path.basename(pathname)