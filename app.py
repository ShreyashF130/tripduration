from pydantic import BaseModel
from fastapi import FastAPI
from joblib import load
import os
import pandas as pd
# from build_features import feature_build
app = FastAPI()

class PredictionInput(BaseModel):
    vendor_id:float
    # pickup_datetime:float
    # dropoff_datetime:float
    passenger_count:float
    pickup_longitude:float
    pickup_latitude:float
    dropoff_longitude:float
    dropoff_latitude:float
    store_and_fwd_flag:float
    # trip_duration:float
    # pickup_date:float
    distance_haversine:float 
    distance_dummy_manhattan:float
    direction:float

print(os.getcwd())
# model_path = "models/model.joblib"
model_path = r"C:\Users\Shreyash\tripduration\tripduration\models\model.joblib"
model = load(model_path)

@app.get("/")
def home():
    return "Working fine"

@app.post("/predict")
def predict(input_data:PredictionInput):
     
     
#      'vendor_id' 'passenger_count' 'pickup_longitude' 'pickup_latitude'
#  'dropoff_longitude' 'dropoff_latitude' 'store_and_fwd_flag'
#  'distance_haversine' 'distance_dummy_manhattan' 'direction']


    features = {
        'vendor_id': input_data.vendor_id,
        'passenger_count': input_data.passenger_count,
        'pickup_longitude': input_data.pickup_longitude,
        'pickup_latitude': input_data.pickup_latitude,
        'dropoff_longitude': input_data.dropoff_longitude,
        'dropoff_latitude': input_data.dropoff_latitude,
        'store_and_fwd_flag': input_data.store_and_fwd_flag,
        'distance_haversine': input_data.distance_haversine,
        'distance_dummy_manhattan': input_data.distance_dummy_manhattan,
        'direction': input_data.direction
    }



    model_path = r"C:\Users\Shreyash\tripduration\tripduration\models\model.joblib"
    loaded_data = load(model_path)

    # Add this line to see the keys in your terminal:
    # print(" Aur ki haal chal => Keys in the loaded file:", loaded_data.keys())



    # print(len(features), features) 
    
    # print(model.feature_names_in_)
    features = pd.DataFrame(features, index=[0])
    features = features[model.feature_names_in_]
    prediction = model.predict(features)[0].item()
    # features = feature_build(features,'prod')
    
    return {"predicted_trip_duration": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8080)
