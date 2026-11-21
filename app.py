from fastapi import FastAPI
from pydantic import BaseModel, Field
import mlflow.sklearn
import numpy as np

app = FastAPI()

# Load the trained model
model = mlflow.sklearn.load_model("./model")

class DigitInput(BaseModel):
    pixels: list[float] = Field(min_length=64, max_length=64)

@app.post("/predict")
def predict(data: DigitInput):
    features = np.array(data.pixels).reshape(1, 64)
    prediction = model.predict(features)[0]
    return {"prediction": int(prediction)}