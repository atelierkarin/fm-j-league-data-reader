import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('raw_data.csv')

df['平均クラブ勝点'] = df['クラブ勝点'] / df['試合数']
df['平均試合出場数'] = df['試合出場数'] / df['試合数']
df['平均得点'] = df['得点'] / df['試合数']

df = pd.get_dummies(df, columns=['POS'])

# Data with CA
df_with_ca = df[df['CA'].notnull()]

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

X = df_with_ca[['POS_GK', 'POS_DF', 'POS_MF', 'POS_FW', '平均クラブ勝点', 'リーグ知名度', '平均試合出場数', '平均得点']].values
y = df_with_ca['CA']

pipe = make_pipeline(MLPRegressor())

param_grid = {
  'mlpregressor__activation': ['tanh'],
  'mlpregressor__solver': ['adam'],
  'mlpregressor__hidden_layer_sizes':[(50, 50), (50, 100), (100, 50), (100, 100)],
  'mlpregressor__alpha': [0.1, 1, 10],
  'mlpregressor__max_iter': [10000]
}

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

grid = GridSearchCV(pipe, param_grid=param_grid, cv=5, verbose=2)
grid.fit(X_train, y_train)
print("-" * 50)
print("\nGrid-Search")
print("Best parameters:", grid.best_params_)
print("Best cross-validation score: {:.3f}".format(grid.best_score_))
print("-" * 50)
scores = grid.score(X_test, y_test)
print("Test set score: {:.2f}".format(scores))
print("-" * 50)
print("Test set accuracy: {:.3f}".format(grid.score(X_test, y_test)))

# Predict and export

predict_X = df[['POS_GK', 'POS_DF', 'POS_MF', 'POS_FW', '平均クラブ勝点', 'リーグ知名度', '平均試合出場数', '平均得点']].values

predict_ca = grid.predict(predict_X)

df['CA_CALC'] = predict_ca

df.to_csv('results.csv',encoding='utf-8-sig')

with open('regional_league_model.pickle', mode='wb') as fp:
  pickle.dump(grid, fp)