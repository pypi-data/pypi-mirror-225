from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd

NON_SCALE_COLS = ['content_model', 'content_edit'] + ['student_reflection_id_model', 'student_user_id_model']

def scale_features(data, model_type, train_flag):
    non_scale_cols_present = [c for c in NON_SCALE_COLS if c in data.columns]
    scale_path = f"/Scalar_{model_type}.joblib"
    data_to_not_scale = data[non_scale_cols_present]
    data_to_scale = data.drop(non_scale_cols_present, axis=1)
    if train_flag == 1:
        scaler = StandardScaler()
        scaler.fit(data_to_scale)
        data_scaled = scaler.transform(data_to_scale)
        joblib.dump(scaler, scale_path)
    else:
        scaler = joblib.load(scale_path)
        data_scaled = scaler.transform(data_to_scale)
    data_scaled = pd.DataFrame(
        data=data_scaled, index=data_to_scale.index, columns=data_to_scale.columns)
    data_scaled[non_scale_cols_present] = data_to_not_scale

    return data_scaled