import numpy as np
import random
import statistics
import scipy.stats as stats

# 1. Income Distribution Dataset (Array 1)
income_data = np.random.normal(50000, 15000, 95).tolist()  # Normal distribution
income_data += [200000, 220000, 250000, 270000, 300000]  # Adding outliers

# 2. Product Rating Dataset (Array 2)
rating_data = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 25, 40, 20], k=50)  # Biased towards 4-star ratings

# 3. Temperature Dataset (Array 3)
temperature_data = np.random.normal(75, 5, 28).tolist()  # Normal distribution around 75°F
temperature_data += [60, 95, 98]  # Adding minor outliers

# Function to calculate and display statistics
def analyze_dataset(dataset, name):
    mean_value = np.mean(dataset)
    median_value = np.median(dataset)
    mode_value = statistics.mode(dataset)
    
    print(f"\n{name} Analysis:")
    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")
    print(f"Mode: {mode_value}")
    
    # Analysis
    if abs(mean_value - median_value) > abs(mode_value - median_value):
        print("Median is more representative due to skewness or outliers.")
    elif mode_value == median_value:
        print("Mode is a good representation, indicating frequent values.")
    else:
        print("Mean is effective when data is normally distributed.")
    
# Analyzing datasets
analyze_dataset(income_data, "Income Distribution")
analyze_dataset(rating_data, "Product Ratings")
analyze_dataset(temperature_data, "Temperature Data")
