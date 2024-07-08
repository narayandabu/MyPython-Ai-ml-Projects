from joblib import load

# vocabulary = load('saves/voca.joblib')
my_pipeline = load('saves/pipeline.joblib')
model = load('saves/model.joblib')


def sol_transform(solns):
    sol = []
    for i in solns:
        if i == 0:
            sol.append('Negative')
        else:
            sol.append('Positive')
    return sol


input_data = ['hellow', 'dead', 'struggle', 'Bad Person', 'accident']  # could be anything or any form

refined_data = my_pipeline.transform(input_data)
predictions = model.predict(refined_data)

predictions = sol_transform(predictions)

print(predictions)
