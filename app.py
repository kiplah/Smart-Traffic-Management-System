from flask import Flask, render_template, jsonify, request
import random
import pandas as pd
import numpy as np

app = Flask(__name__)

# Function to simulate traffic data (vehicle count and average speed at each intersection)
def get_traffic_data():
    intersections = ["A", "B", "C", "D"]
    traffic_data = {
        "intersection": intersections,
        "vehicle_count": [random.randint(50, 200) for _ in intersections],
        "avg_speed": [random.randint(10, 60) for _ in intersections],  # Speed in km/h
    }
    return pd.DataFrame(traffic_data)

# Function to predict traffic congestion (based on vehicle count and average speed)
def predict_congestion(traffic_data):
    congestion_level = {}
    for index, row in traffic_data.iterrows():
        # A simple model: Higher vehicle count and lower speed = higher congestion
        congestion_score = (row['vehicle_count'] / 200) * (60 - row['avg_speed']) / 60
        if congestion_score > 0.7:
            congestion_level[row['intersection']] = 'High'
        elif congestion_score > 0.4:
            congestion_level[row['intersection']] = 'Medium'
        else:
            congestion_level[row['intersection']] = 'Low'
    return congestion_level

# Function to adjust signal timings based on congestion prediction
def adjust_signal_timings(congestion_level):
    signal_timing = {}
    for intersection, level in congestion_level.items():
        if level == 'High':
            signal_timing[intersection] = 30  # 30 seconds green light
        elif level == 'Medium':
            signal_timing[intersection] = 20  # 20 seconds green light
        else:
            signal_timing[intersection] = 15  # 15 seconds green light
    return signal_timing

@app.route('/')
def index():
    # Get the traffic data (simulated for now)
    traffic_data = get_traffic_data()
    return render_template('index.html', traffic_data=traffic_data)

@app.route('/adjust_signals', methods=['POST'])
def adjust_signals():
    # Get the current traffic data (simulated)
    traffic_data = get_traffic_data()
    
    # Predict congestion levels based on traffic data
    congestion_level = predict_congestion(traffic_data)
    
    # Adjust signal timings based on congestion levels
    signal_timings = adjust_signal_timings(congestion_level)
    
    # Respond with the congestion levels and adjusted signal timings
    response = {
        'congestion_level': congestion_level,
        'signal_timings': signal_timings
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
