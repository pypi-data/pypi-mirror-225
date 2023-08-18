import gensim
import pandas as pd
import numpy as np

ALERTS = 'alerts'
W2V_50 = gensim.models.KeyedVectors.load_word2vec_format("word2vec.txt", binary=False)
W2V_100 = gensim.models.KeyedVectors.load_word2vec_format("glove.6B.100d.txt", binary=False)


def create_w2v_features(text_column, w2v=W2V_50, project=None):
    filters = get_filters(project)
    words = gensim.parsing.preprocessing.preprocess_string(text_column, filters)
    vecs = get_vectors(words, w2v)

    return np.concatenate([np.max(vecs, 1),
                           np.min(vecs, 1),
                           np.sum(vecs, 1)])

def get_vectors(words, w2v):
    vecs = []
    for word in words:
        neg_multiplier = 1
        if '_' in word:
            word = word.split('_')[1]
            neg_multiplier = -1
        if word in w2v.key_to_index:
            w_vec = neg_multiplier * w2v.get_vector(word)
            vecs.append(w_vec)
    if not vecs:
        vecs.append(np.zeros(w2v.vector_size))
    return np.stack(vecs, 1)


def get_filters(project):
    if project == ALERTS:
        return (gensim.parsing.preprocessing.strip_tags,
                gensim.parsing.preprocessing.strip_multiple_whitespaces,
                gensim.parsing.preprocessing.strip_numeric
                )
    return (gensim.parsing.preprocessing.strip_tags,
            gensim.parsing.preprocessing.strip_punctuation,
            gensim.parsing.preprocessing.strip_multiple_whitespaces,
            gensim.parsing.preprocessing.strip_numeric
            )


def get_w2v(dimensions):
    if dimensions == 100:
        return W2V_100
    return W2V_50


def transform_df(text_column, dimensions=50, project=None):
    w2v = get_w2v(dimensions)
    return pd.DataFrame(list(map(np.ravel,
                                 text_column.apply(create_w2v_features, args=(w2v, project, ))
                                 ))).add_prefix('WordEmbeddingFeature_')
