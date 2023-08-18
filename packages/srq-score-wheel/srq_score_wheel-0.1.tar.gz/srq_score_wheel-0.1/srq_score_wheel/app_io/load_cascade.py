import mlflow
from mlflow.tracking import MlflowClient
from collections import defaultdict
import en_core_web_sm
import pickle

# Make sure to check j in (i, j) in registered_model_names where j should match with run_name in experiment
registered_model_names = [('NB','srq_nb'), ('SVM','srq_svm'), ('KNN','srq_knn'), ('XGB','srq_xgb'), 
                          ('RF_0','srq_rf_class_0'), ('RF_1','srq_rf_class_1'), ('RF_2','srq_rf_class_2'), 
                          ('RF_3','srq_rf_class_3'), ('RF_4','srq_rf_class_4')]

def get_model_path(registered_model_names):

    model_paths = defaultdict()
    client = MlflowClient()

    for i, j in registered_model_names:
        registered_model = client.get_registered_model(j)
        model_uri = registered_model.latest_versions[0].source
        model_paths[i] = model_uri
    
    return model_paths

def load_models():

    model_paths = get_model_path(registered_model_names)

    models = defaultdict(list)
    models = {'RF': []}

    for i, j in model_paths.items():
        if i == 'XGB':
            models[i] = [mlflow.xgboost.load_model(j)]
        elif i not in ['RF_0', 'RF_1', 'RF_2', 'RF_3', 'RF_4']:
            models[i] = [mlflow.sklearn.load_model(j)]
        else:
            models['RF'].append(mlflow.sklearn.load_model(j))

    return models

def load_feature_dicts():
    feature_dicts = dict()
    feature_dicts["POS_FAMILY"] = pickle.load(open(mod.POS_FAMILY_PATH, 'rb'))
    feature_dicts["PHRASE_FAMILY"] = pickle.load(open(mod.PHRASE_FAMILY_PATH, 'rb'))
    feature_dicts["NLP_DICT"] = en_core_web_sm.load()

    smart_word_feature_names = ["aas", "olc",
                                "ccp", "slp", "tcs", "csr", "ese", "ecr"]

    feature_dicts["SMART_FAMILY"] = dict.fromkeys(smart_word_feature_names)
    for feature in smart_word_feature_names:
        feature_dicts["SMART_FAMILY"][feature] = pickle.load(
            open(mod.SMART_FAMILY_PATH + feature, 'rb'))
    
    return feature_dicts