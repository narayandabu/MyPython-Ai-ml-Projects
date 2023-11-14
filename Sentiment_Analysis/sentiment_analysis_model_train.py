import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from joblib import dump
from sklearn.pipeline import Pipeline

pos_neg_data = pd.read_excel("./Data/LabeledText.xlsx", engine="openpyxl")

my_pipeline = Pipeline(steps=[
    ('count_vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
])

labels = {
    'positive': 1.0,
    'negative': 0.0,
}

pos_neg_data = pos_neg_data[pos_neg_data['LABEL'] != 'neutral']
pos_neg_data.replace(labels, inplace=True)

x = np.array(pos_neg_data['Caption'])
y = np.array(pos_neg_data['LABEL'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

x_train_tfidf = my_pipeline.fit_transform(x_train)
x_test_tfidf = my_pipeline.transform(x_test)
vocabulary = my_pipeline.get_feature_names_out()
print(x_test_tfidf, ' ', y_test)

model = MultinomialNB()
model.fit(x_train_tfidf, y_train)
predicted = model.predict(x_test_tfidf)
score = accuracy_score(y_test, predicted)

dump(model, 'saves/model.joblib')
dump(vocabulary, 'saves/voca.joblib')
dump(my_pipeline, 'saves/pipeline.joblib')

print("Score:- ", score * 100, "%")
