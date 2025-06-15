import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("businesses.csv")

# ✍️ Добавь вручную колонку success (1 — успешный бизнес, 0 — нет)

X = df.drop("success", axis=1)
y = df["success"]

X.to_csv("training/X.csv", index=False)
y.to_csv("training/y.csv", index=False)