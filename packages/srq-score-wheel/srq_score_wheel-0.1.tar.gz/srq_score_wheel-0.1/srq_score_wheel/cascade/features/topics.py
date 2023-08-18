import gensim
from gensim import corpora
import pandas as pd

def create_topic_features(data, nlp_dict, num_topics=4):
    texts = prepare_for_tm_opt(data["content_edit"], nlp_dict)
    id2word = corpora.Dictionary(texts)
    corpus = [id2word.doc2bow(text) for text in texts]
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=20,
                                                alpha='auto',
                                                per_word_topics=False)
    topic_model_objects = {"lda_model": lda_model,
                           "id2word": id2word,
                           "num_topics": num_topics}
    return topic_model_objects


def predict_topic_features(data, nlp_dict, lda_model, id2word):
    list_arrays = [
        lda_model.get_document_topics(
            id2word.doc2bow(content)) for content in prepare_for_tm_opt(
                data["content_edit"], nlp_dict)]
    topics = pd.DataFrame([[topic_prob[1] for topic_prob in docs]
                           for docs in list_arrays]).add_prefix('topic_')

    return pd.concat([data.reset_index(drop=True),
                      topics.reset_index(drop=True)], axis=1)


def is_token_valid_for_tm(token):
    return not token.is_punct or token.is_space or token.is_stop or len(token.text) <= 4


def prepare_for_tm_opt(docs, nlp):
    filtered_tokens = []
    for doc in nlp.pipe(docs):
        tokens = [token.lemma_ for token in doc if (is_token_valid_for_tm(token) and token.pos_ in [
            'NOUN', 'ADJ', 'ADV', 'AUX', 'CONJ', 'PRON'])]
        filtered_tokens.append(tokens)
    return filtered_tokens