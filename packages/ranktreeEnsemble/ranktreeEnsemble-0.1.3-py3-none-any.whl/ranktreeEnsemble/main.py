from ranktreeEnsemble.data.dataPrep import *
from ranktreeEnsemble.Method.ranktreeMethod import *
import pandas as pd

tnbc = pd.read_csv("data/tnbc.csv")

model = rforest(tnbc.drop(columns=['subtype']).head(100), tnbc["subtype"].head(100))
# get feature importance scores:
model.feature_importances_

# pair() to convert continuous variables to binary ranked pairs:
datp = pair(tnbc.iloc[100:111,:-1])
print(datp)
model.predict(datp)

# Build a Boosting with LogitBoost Cost model with Variable Importance:
model = rboost(tnbc.drop(columns=['subtype']).head(100), tnbc["subtype"].head(100))
# get feature importance scores:
model.feature_importances_
# Build a Boosting with LogitBoost Cost model with forward stepwise feature selection:
model_rfa = rboost_rfa(tnbc.drop(columns=['subtype']).head(100), tnbc["subtype"].head(100))
# Build a Boosting with LogitBoost Cost model with backward stepwise feature selection:
model_rfe = rboost_rfe(tnbc.drop(columns=['subtype']).head(100), tnbc["subtype"].head(100))

