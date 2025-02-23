from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from flask_cors import CORS  # To allow frontend requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Sample dataset (Temperature vs. Ice Cream Sales)
data = 'ice.csv'
df = pd.DataFrame(data)

# Extract X (features) and y (target variable)
X = np.array(df["Temperature"]).reshape(-1, 1)
y = np.array(df["Sales"])

# Split dataset into training (70%) and testing (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Train the Linear Regression model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Calculate model accuracy (R² score)
y_pred_test = regressor.predict(X_test)
r2 = r2_score(y_test, y_pred_test)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        temperature = float(data["temperature"])
        predicted_sales = regressor.predict(np.array([[temperature]]))[0]

        return jsonify({
            "predicted_sales": round(predicted_sales, 2),
            "r2_score": round(r2, 4)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
