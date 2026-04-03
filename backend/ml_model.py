from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([[1,0],[2,1],[0,2],[3,1]])
y = [1,1,0,1]

model = LogisticRegression()
model.fit(X, y)

def predict(home, away):
    return "Win" if model.predict([[home, away]])[0] else "Lose"