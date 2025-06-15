import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.services.preprocess import vectorize

df = pd.read_csv("businesses.csv")
df_vectors = vectorize(df)

def recommend_alternative(input_data):
    input_vector = vectorize(pd.DataFrame([input_data.dict()]))
    sims = cosine_similarity(input_vector, df_vectors)[0]
    best_idx = sims.argmax()
    return df.iloc[best_idx].to_dict()