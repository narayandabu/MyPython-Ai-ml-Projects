from joblib import load

vocabulary = load('voca.joblib')
my_pipeline = load('pipeline.joblib')


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

refined_data = my_pipeline.transform(input_data)
predictions = model.predict(refined_data)

predictions = sol_transform(predictions)

print(predictions)
