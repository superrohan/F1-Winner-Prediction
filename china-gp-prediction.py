#Author: Rohan Bangera

import os
import fastf1 as f1 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


cache_dir = "f1_cache"
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir) 

# Enable FastF1 caching
f1.Cache.enable_cache("f1_cache")

# Load 2024 China GP Race Data
session_2024 = f1.get_session(2024, "China", "R")
session_2024.load()

# Extract lap times
laps_2024 = session_2024.laps[["Driver", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]].copy()
laps_2024.dropna(subset=["LapTime"], inplace=True)
#laps_2024["LapTime (s)"] = laps_2024["LapTime"].dt.total_seconds()

#Convert times to seconds
for col in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
    laps_2024[f"{col} (s)"] = laps_2024[col].dt.total_seconds()

#Group by driver to get average sector times per driver
sector_times_2024 = laps_2024.groupby("Driver")[["LapTime (s)","Sector1Time (s)", "Sector2Time (s)", "Sector3Time (s)"]].mean().reset_index()


#2025 Qualifying Data
qualifying_2025 = pd.DataFrame({
     "Driver": ["Oscar Piastri", "George Russell", "Lando Norris", "Max Verstappen", "Lewis Hamilton", 
               "Charles Leclerc", "Yuki Tsunoda", "Alex Albon", 
               "Esteban Ocon", "Nico Hulkenberg", "Fernando Alonso", "Lance Stroll", "Carlos Sainz", 
               "Pierre Gasly"],
    "QualifyingTime (s)": [90.641, 90.723, 90.793, 90.817, 90.927, 
                           91.021, 91.638, 91.706, 
                           91.625, 91.632, 91.688, 91.773, 91.840, 
                           91.992]
})

#Map full anmes to fast-F1 3-letter codes

#driver_mapping = {
#    "Lando Norris": "NOR", "Oscar Piastri": "PIA", "Max Verstappen": "VER", "George Russell": "RUS", "Lewis Hamilton": "HAM",
#    "Charles Leclerc": "LEC", "Yuki Tsunoda": "TSU", "Alexander Albon": "ALB", "Carlos Sainz": "SAI", "Fernando Alonso": "ALO",
#    "Lance Stroll": "STR", "Pierre Gasly": "GAS", "Esteban Ocon": "OCO", "Nico Hulkenberg": "HUL", "Andrea Kimi Antonelli": "ANT",
#    "Isack Hadjar": "HAD", "Liam Lawson": "LAW", "Jack Doohan": "DOO", "Oliver Bearman": "BEA", "Gabriel Bortoleto": "BOR"
#}

driver_mapping = {
    "Lando Norris": "NOR", "Oscar Piastri": "PIA", "Max Verstappen": "VER", "George Russell": "RUS", "Lewis Hamilton": "HAM",
    "Charles Leclerc": "LEC", "Yuki Tsunoda": "TSU", "Alexander Albon": "ALB", "Carlos Sainz": "SAI", "Fernando Alonso": "ALO",
    "Lance Stroll": "STR", "Pierre Gasly": "GAS", "Esteban Ocon": "OCO", "Nico Hulkenberg": "HUL"
}

qualifying_2025["DriverCode"] = qualifying_2025["Driver"].map(driver_mapping)

#Merge 2025 Qualifying Data with 2024 race data
merged_data = qualifying_2025.merge(sector_times_2024, left_on="DriverCode", right_on="Driver")


#Use only 'Qualifying Time (s) as a feature'
X = merged_data[["QualifyingTime (s)"]]
y = merged_data["LapTime (s)"]

if X.shape[0] == 0:
    raise ValueError("Dataset is empty after preprocessing, Check data sources!")

#Train Gradient Boosting Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=39)
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=39)
model.fit(X_train, y_train)

#Predict using 2025 qualifying times
predicted_lap_times = model.predict(qualifying_2025[["QualifyingTime (s)"]])
qualifying_2025["PredictedRaceTime (s)"] = predicted_lap_times

#Rank drivers by predicted race time
qualifying_2025 = qualifying_2025.sort_values(by="PredictedRaceTime (s)")

#Print final predictions
print("\n 🏆 Predicted Winner of the 2025 Chinese GP: \n")
print(qualifying_2025[["Driver", "PredictedRaceTime (s)"]])

#Evaluate Model
y_pred = model.predict(X_test)
print(f"\n Model Error (MAE): {mean_absolute_error(y_test, y_pred):.2f} seconds")