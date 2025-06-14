import pandas as pd
import numpy as np

df_minacov = pd.read_csv("data/df_train_for_cv_minacov.csv")
df_baryshev = pd.read_csv("data/df_train_for_cv_baryshev.csv")
df_almetov = pd.read_csv("data/df_train_for_cv_almetov.csv")

df = pd.concat([df_almetov, df_baryshev, df_minacov])
print(df.groupby('label').size())
