import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Create a tiny dataset to start
data = {
    'url_length': [15, 100, 20, 120, 18, 150],
    'has_at_symbol': [0, 1, 0, 1, 0, 1],
    'is_phishing': [0, 1, 0, 1, 0, 1]  # 0 = Safe, 1 = Phishing
}
df = pd.DataFrame(data)

# 2. Train the Model
X = df[['url_length', 'has_at_symbol']]
y = df['is_phishing']

model = RandomForestClassifier()
model.fit(X, y)

# 3. Save it
if not os.path.exists('models'):
    os.makedirs('models')
joblib.dump(model, 'models/phish_model.pkl')
print("✅ Model trained and saved in models/phish_model.pkl")