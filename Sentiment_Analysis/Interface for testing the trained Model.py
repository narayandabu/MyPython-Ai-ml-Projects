from joblib import load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

vocabulary = load('voca.joblib')


def covert_to_tfdif(data):
    count_vect = CountVectorizer(vocabulary=vocabulary)
    tfidf_transformer = TfidfTransformer()
    tfidf = count_vect.fit_transform(data)
    tfidf = tfidf_transformer.fit_transform(tfidf)
    return tfidf


def sol_transform(solns):
    sol = []
    for i in solns:
        if i == 0:
            sol.append('Negative')
        else:
            sol.append('Positive')
    return sol


model = load('model.joblib')
input_data = ['hellow', 'bad', 'struggle', 'lose']  # could be anything or any form

refined_data = covert_to_tfdif(input_data)
predictions = model.predict(refined_data)

predictions = sol_transform(predictions)

print(list(predictions))
