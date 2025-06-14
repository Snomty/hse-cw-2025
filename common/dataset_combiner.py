import pandas as pd

df_minacov = pd.read_csv("data/df_train_for_cv_minacov.csv")
df_baryshev = pd.read_csv("data/df_train_for_cv_baryshev.csv")
df_almetov = pd.read_csv("data/df_train_for_cv_almetov.csv")

df = pd.concat([df_almetov, df_baryshev, df_minacov])
print(df.groupby('label').size())
print(f"\ntotal tagged photo:\t{df.shape[0]}")
print(f"total useful tagged photo:\t{df[df['label'] != 0].shape[0]}")

df = df[df['label'] != 0]
df.to_csv("data/df_train_for_cv.csv", index=False)
