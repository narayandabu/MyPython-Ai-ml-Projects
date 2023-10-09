import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from joblib import dump

df = pd.read_csv('./Data/cleandata.csv')
df = df.drop(['Tweets', 'Date'], axis=1)
pos_neg_data = pd.read_excel("./Data/LabeledText.xlsx", engine="openpyxl")
df1 = df.copy(deep=True)


def normalize_data(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def split_single(data):
    for tweet in data:
        x = tweet
        if len(str(x).split()) > 1:
            df.drop(df[df['Cleaned_Tweets'] == tweet].index, inplace=True)


def remove_some(data):
    x = data.split()
    new_str = ""
    for i in x:
        if i[0] == '#':
            new_str = new_str + ' ' + i[1:len(i)]
        else:
            new_str = new_str + ' ' + i
    return new_str


for data in pos_neg_data['Caption']:
    trimmed_data = remove_some(data)
    pos_neg_data['Caption'].replace(data, trimmed_data, inplace=True)

labels = {
    'positive': 1.0,
    'negative': 0.0,
}

pos_neg_data = pos_neg_data[pos_neg_data['LABEL'] != 'neutral']
pos_neg_data.replace(labels, inplace=True)

x = np.array(pos_neg_data['Caption'])
y = np.array(pos_neg_data['LABEL'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

x_train_tfidf = count_vect.fit_transform(x_train)
x_train_tfidf = tfidf_transformer.fit_transform(x_train_tfidf)

x_test_tfidf = count_vect.transform(x_test)
x_test_tfidf = tfidf_transformer.transform(x_test_tfidf)

vocabulary = count_vect.get_feature_names_out()
print(vocabulary)

print(x_train_tfidf.shape, x_test_tfidf.shape)

model = MultinomialNB()
model.fit(x_train_tfidf, y_train)

predicted = model.predict(x_test_tfidf)
score = accuracy_score(y_test, predicted)
dump(model, 'model.joblib')
dump(vocabulary,'voca.joblib')
print("Score:- ", score * 100, "%")
