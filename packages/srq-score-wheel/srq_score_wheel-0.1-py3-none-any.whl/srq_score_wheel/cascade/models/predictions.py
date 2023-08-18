import sys
import os
sys.path.append('/Workspace/Repos/developers@sowntogrow.com/sown-ml-2023/wheel_development')
from srq_score_wheel.env_setup import RESOURCE_PATH_ABS, ENV    
sys.path.append(os.path.abspath(RESOURCE_PATH_ABS))

from multiprocessing import Process, Pipe
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold

# Import resources based on env
if ENV == 'dev':
    import dev_resources as mod
elif ENV == 'prod':
    import prod_resources as mod

from srq_score_wheel.cascade.features.model import append_model_features
from srq_score_wheel.cascade.features.scale import scale_features
from srq_score_wheel.cascade.features.word2vec import transform_df
from srq_score_wheel.cascade.features import words
from srq_score_wheel.cascade.features.words import combine_word_features
from srq_score_wheel.cascade.models.aux import (drop_id_cols,
                                          get_xgb_features,
                                          get_top1_top2,
                                          get_tops,
                                          CLASSES,
                                          append_columns)
from srq_score_wheel.cascade.reflections.content import extract_edited_content

FEATURES_TO_CREATE = [words.create_meta,
                      words.create_phrase_based,
                      words.create_pos_tag,
                      words.create_smart_word]
FEATURES_TO_DROP = ["rating_model",  # 'content', 'content_edit',
                    "goal_notes_model", "score_model", 'prompt_model',  # 'student_user_id_model',
                    'updated_at_model', 'scored_performance_model',
                    'classroom_activity_pairing_id_model', 'id_model',
                    'scored_performance_model', 'completed_performance_model',
                    'performance_date_model', 'created_at_model', 'goal_met_model',
                    'activity_level_id_model', 'student_performance_id_model']
XGB_TO_KEEP_FEATURES = ['activity_type_model', 'char_count', 'comma_count',
                        'exclaim_count', 'goal_notes_char_count', 'punctuation_count',
                        'stop_count', 'word_count', 'ownership_words', 'strategy_words']
KNN_TO_KEEP_FEATURES = ['goal_level_model', 'future_count', 'reflection_type_model',
                        'activity_type_model', 'change_words',
                        'because_words', 'past_count',
                        'may_be_words', 'but_words', 'positive_freq_words',
                        'goal_notes_char_count', 'emphasis_words',
                        'strategy_words', 'noun_count', 'improve_words',
                        'neutral_freq_words', 'that_words',  # 'rating',
                        'word_count', 'no_words', 'and_words',
                        'my_work_words', 'people_words', 'ownership_words', 'punctuation_count',
                        'numerical_count', 'time_words', 'for_words',
                        'will_words', 'try_words', 'stop_count', 'pron_count',
                        'grade_words', 'exclaim_count', 'this_words', 'the_words',
                        'do_words', 'if_words', 'negative_freq_words', 'hard_words',
                        'adv_count', 'adj_count', 'char_count',
                        'verb_count', 'comma_count',
                        'topic_0', 'topic_1', 'topic_2', 'topic_3',
                        'csr', 'ccp', 'aas', 'olc', 'slp', 'ecr', 'tcs', 'ese',
                        'SVM_Pred_Top_1', 'SVM_Pred_Top_2', 'NB_Pred_Top_1', 'NB_Pred_Top_2']
RF_TO_KEEP_FEATURES = ['goal_level_model', 'future_count', 'reflection_type_model',
                       'activity_type_model', 'change_words',
                       'because_words', 'past_count',
                       'may_be_words', 'but_words', 'positive_freq_words',
                       'goal_notes_char_count', 'emphasis_words',
                       'strategy_words', 'noun_count', 'improve_words',
                       'neutral_freq_words', 'that_words',  # 'rating',
                       'and_words', 'word_count', 'no_words',
                       'my_work_words', 'people_words', 'ownership_words', 'punctuation_count',
                       'numerical_count', 'time_words', 'for_words',
                       'will_words', 'try_words', 'stop_count', 'pron_count',
                       'grade_words', 'exclaim_count', 'this_words', 'the_words',
                       'do_words', 'if_words', 'negative_freq_words', 'hard_words',
                       'adv_count', 'adj_count', 'char_count',
                       'verb_count', 'comma_count',
                       'topic_0', 'topic_1', 'topic_2', 'topic_3',
                       'csr', 'ccp', 'aas', 'olc', 'slp', 'ecr', 'tcs', 'ese',
                       'SVM_Pred_Top_1', 'SVM_Pred_Top_2', 'XGB_Pred_Top_1', 'XGB_Pred_Top_2',
                       'KNN_Pred_Top_1', 'KNN_Pred_Top_2']

def predict_cascade(features, data_y, n_folds, model, prediction_fn, params):
    skf = StratifiedKFold(n_folds)
    cascade_data = pd.DataFrame()
    cascade_flag = pd.DataFrame()
    for train_index, test_index in skf.split(features, data_y.score_model):
        data_test_fold, y_pred_fold = train_predict_cascade_fold(
            features, data_y, train_index, test_index, model, prediction_fn, params)
        cascade_flag = pd.concat([cascade_flag, y_pred_fold])
        cascade_data = pd.concat([cascade_data, data_test_fold])

    return cascade_data, cascade_flag

def train_predict_cascade_fold(features, data_y , train_index, test_index, model, prediction_fn, params):
    y_train_fold, __ = data_y.iloc[train_index], data_y.iloc[test_index]
    features_train_fold, features_test_fold = features.iloc[train_index], features.iloc[test_index]
    clf, __ = model(features_train_fold, y_train_fold, params)
    y_pred_fold = prediction_fn(features_test_fold, [clf])
    
    return features_test_fold, y_pred_fold

def get_predictions(agg_data_pred_orig, models, feature_dicts, train_flag=0):

    all_features = get_all_features(agg_data_pred_orig.copy(), feature_dicts, train_flag=train_flag)

    svm_model_features = pred_svm(agg_data_pred_orig, models["SVM"])
    nb_model_features = pred_nb(agg_data_pred_orig, models["NB"])
    xgb_model_features = pred_xgb(all_features, models["XGB"])
    knn_features_scaled = scale_features(all_features, "KNN", train_flag=train_flag)
    knn_prediction_features = append_model_features(knn_features_scaled,
                                                    [svm_model_features,
                                                    nb_model_features])

    knn_model_features = pred_knn(knn_prediction_features.copy(), models["KNN"])
    rf_prediction_features = append_model_features(all_features,
                                                   [svm_model_features,
                                                   xgb_model_features,
                                                   knn_model_features])
    
    output = pred_rf(rf_prediction_features, models["RF"])

    return output


def get_all_features(agg_data_train, feature_dicts, train_flag=0):

    return combine_word_features(
        agg_data_train.copy(deep=False),
        feature_dicts,
        features_to_drop=FEATURES_TO_DROP,
        features_to_create=FEATURES_TO_CREATE,
        model_type="RF",
        topic_model_features_flag=1,
        scale_features_flag=0,
        train_flag=train_flag).replace([np.inf, -np.inf],
                                       np.nan).fillna(0)


def make_predictions(modelnames, data, model_type):
    if model_type == "RF":
        return pd.concat(
            [x.reset_index(drop=True) for x in get_parallelized_rf_preds(modelnames, data)], axis=1)

    for modelname in modelnames:
        prob_predictions = pd.DataFrame(modelname.predict_proba(data))

    return prob_predictions


def get_parallelized_rf_preds(modelnames, data):
    pipe_list = []
    recv_end, send_end = Pipe(False)
    running_tasks = [Process(target=get_one_rf_preds, args=(idx, modelname, data, send_end)) for idx, modelname in enumerate(modelnames)]

    for running_task in running_tasks:
        running_task.start()
    
    for running_task in running_tasks:
        try:
            pipe_list.append(recv_end.recv())
            running_task.join(0.01)
        except EOFError:
            break
    
    return pipe_list


def get_one_rf_preds(idx, modelname, data, send_end):
    probs = pd.DataFrame()
    probs[idx] = modelname.predict_proba(data)[::, 1]
    send_end.send(probs[idx])


def format_predictions(prob_predictions, dataid, model_type, get_top1_top2_flag=1):

    max_likelihood = pd.Series(prob_predictions.max(axis=1))
    abs_predictions = pd.Series(get_tops(prob_predictions, 1, CLASSES))

    results = (pd.concat([dataid.reset_index(drop=True),
                          pd.DataFrame({'abs_predictions': abs_predictions,
                                        'max_likelihood': max_likelihood}).reset_index(drop=True),
                          prob_predictions.reset_index(drop=True)], axis=1))

    return get_top1_top2(model_type, results) if get_top1_top2_flag == 1 else results


def pred_xgb(agg_data_pred_orig, xgb_models):
    model_type = "XGB"
    dataid = drop_id_cols(agg_data_pred_orig.copy(deep=False))["dataid"]

    xgb_word_embed_features = transform_df(agg_data_pred_orig["content_model"].copy(deep=False))
    xgb_features = append_columns(agg_data_pred_orig[XGB_TO_KEEP_FEATURES], xgb_word_embed_features)

    xgb_data = get_xgb_features(drop_id_cols(xgb_features)["data"])
    prob_predictions = make_predictions(xgb_models, xgb_data, model_type=model_type)

    return format_predictions(prob_predictions, dataid, model_type, get_top1_top2_flag=1)


def pred_svm(agg_data_pred_orig, svm_models):
    model_type = "SVM"
    dataid = drop_id_cols(agg_data_pred_orig.copy(deep=False))["dataid"]

    agg_data_pred_orig.loc[:, 'content_edit'] = extract_edited_content(agg_data_pred_orig["content_model"])
    svm_features = agg_data_pred_orig.content_edit

    prob_predictions = make_predictions(svm_models, svm_features, model_type=model_type)

    return format_predictions(prob_predictions, dataid, model_type, get_top1_top2_flag=1)


def pred_nb(agg_data_pred_orig, nb_models):
    model_type = "NB"
    dataid = drop_id_cols(agg_data_pred_orig.copy(deep=False))["dataid"]

    agg_data_pred_orig.loc[:, 'content_edit'] = extract_edited_content(agg_data_pred_orig["content_model"])
    nb_features = agg_data_pred_orig.content_edit

    prob_predictions = make_predictions(nb_models, nb_features, model_type=model_type)

    return format_predictions(prob_predictions, dataid, model_type, get_top1_top2_flag=1)


def pred_knn(knn_prediction_features, knn_models):
    model_type = "KNN"
    dataid = drop_id_cols(knn_prediction_features.copy(deep=False))["dataid"]
    knn_data = drop_id_cols(knn_prediction_features.copy(deep=False))["data"]

    prob_predictions = make_predictions(knn_models, knn_data[KNN_TO_KEEP_FEATURES], model_type=model_type)

    return format_predictions(prob_predictions, dataid, model_type, get_top1_top2_flag=1)


def pred_rf(rf_prediction_features, rf_models):
    model_type = "RF"
    dataid = drop_id_cols(rf_prediction_features.copy(deep=False))["dataid"]
    rf_data = drop_id_cols(rf_prediction_features.copy(deep=False))["data"]

    prob_predictions = make_predictions(rf_models, rf_data[RF_TO_KEEP_FEATURES], model_type=model_type)

    return format_predictions(prob_predictions, dataid, model_type,get_top1_top2_flag=1)