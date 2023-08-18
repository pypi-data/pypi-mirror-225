import string
import pickle
import pandas as pd
import numpy as np
import textblob
from nltk import pos_tag_sents, word_tokenize

from srq_score_wheel.cascade.features.topics import create_topic_features, predict_topic_features
from srq_score_wheel.cascade.features.scale import scale_features
from srq_score_wheel.cascade.models.aux import drop_id_cols, append_columns
from srq_score_wheel.cascade.reflections.content import extract_edited_content

META_FEATURE_NAMES = [
    "activity_type_model",
    "char_count",
    "comma_count",
    "content_model",
    "exclaim_count",
    "goal_notes_char_count",
    "punctuation_count",
    "stop_count",
    "word_count"]

def remove_duplicates(list_w_duplicates):
    return list(set(list_w_duplicates))


def create_meta(data, _):
    # Doesn't use feature_dict for this function, hence _ in the second argument

    data["activity_type_model"] = np.where(
        data["activity_type_model"] == "completion", 1, 0)
    data"content_model"] = data["content_model"].replace("'", '')
    data["goal_notes_model"] = data["goal_notes_model"].fillna("a")
    data["goal_notes_char_count"] = count_characters(data["goal_notes_model"])
    data["char_count"] = data["content_model"].apply(len)
    data["comma_count"] = count_punctuations(data["content_model"], ",")
    data["stop_count"] = count_punctuations(data["content_model"], ".")
    data["exclaim_count"] = count_punctuations(data["content_model"], "!")
    data["word_count"] = count_characters(data["content_model"])
    data['punctuation_count'] = data["content_model"].apply(
        lambda x: len("".join(_ for _ in x if _ in string.punctuation)))

    return data, META_FEATURE_NAMES


def count_punctuations(content, punctuation):
    return content.apply(lambda x: x.count(punctuation))


def count_characters(content):
    return content.str.split().str.len()


def create_phrase_based(data, feature_dicts):
    phrase_based_feature_names = []
    for key, value in feature_dicts["PHRASE_FAMILY"].items():
        data[key] = get_feature_counts(data, value)
        phrase_based_feature_names.append(key)
    return data, phrase_based_feature_names


def create_pos_tag(data, feature_dicts):
    pos_tag_feature_names = ["noun_count", "verb_count", "adj_count",
                             "adv_count", "pron_count", "past_count",
                             "future_count", "numerical_count"]
    texts = data["content_model"].tolist()
    tagged_texts = pos_tag_sents(map(word_tokenize, texts))
    for feature in pos_tag_feature_names:
        data[feature] = get_tag_counts(feature.split(
            '_')[0], tagged_texts, feature_dicts["POS_FAMILY"])
    return data, pos_tag_feature_names


def get_tag_counts(feature, tagged_texts, pos_family):
    return pd.Series(tagged_texts).astype(str).str.count(r'|'.join(pos_family[feature]))


def create_smart_word(data, feature_dicts):
    '''Creating features based on https://www.smart-words.org/linking-words/transition-words.html'''

    smart_word_feature_names = ["aas", "olc",
                                "ccp", "slp", "tcs", "csr", "ese", "ecr"]
    for feature in smart_word_feature_names:
        data[feature] = get_feature_counts(
            data, feature_dicts["SMART_FAMILY"][feature])

    return data, smart_word_feature_names


def create_sentiment_feature(data):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    return data.apply(
        lambda x: analyser.polarity_scores(
            x["content"])["compound"], axis=1)


def check_pos_tag(text, flag):
    # pylint: disable=W0703
    # Catching too general exception BaseException (broad-except)
    pos_family = pickle.load(open(f"pos_family", 'rb'))
    cnt = 0
    try:
        wiki = textblob.TextBlob(text)
        for tup in wiki.tags:
            ppo = list(tup)[1]
            if ppo in pos_family[flag]:
                cnt += 1
    except BaseException:
        pass
    return cnt


def combine_word_features(
        agg_data_train,
        feature_dicts,
        features_to_drop,
        features_to_create,
        model_type,
        **flags):
    data = agg_data_train.copy()
    data['content_edit'] = extract_edited_content(
        data["content_model"])
    feature_dict = {}

    # create features
    for feature in features_to_create:
        data, feature_dict[feature.__name__] = feature(data, feature_dicts)
    if flags['topic_model_features_flag'] == 1:
        data = combine_topic_features(data, flags, feature_dicts["NLP_DICT"])

    # drop columns
    results = drop_features(data, features_to_drop)

    # scale features
    if flags['scale_features_flag'] == 1:
        dataid = drop_id_cols(results)["dataid"]
        scaled_results = scale_features(
            drop_id_cols(results)["data"], model_type, train_flag=flags['train_flag'])
    return append_columns(dataid, scaled_results) if flags['scale_features_flag'] == 1 else results


def combine_topic_features(data, flags, nlp_dict):
    topic_model_objects = {}

    for key in ["lda_model", "id2word"]:
        object_path = f"{key}"
        if flags['train_flag'] == 1:
            topic_model_objects[key] = create_topic_features(data, nlp_dict, num_topics=4)[
                key]
            with open(object_path, 'wb') as file:
                pickle.dump(topic_model_objects[key], file)
        else:
            with open(object_path, 'rb') as file:
                topic_model_objects[key] = pickle.load(file)

    data = predict_topic_features(data, nlp_dict, **topic_model_objects)

    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.fillna(0, inplace=True)

    return data


def drop_features(data, features_to_drop):
    features = list(set(data.columns) - set(features_to_drop))
    return data[features]


def get_feature_counts(data, feature_dict):
    return data["content_model"].str.lower().str.count(r'|'.join(feature_dict))