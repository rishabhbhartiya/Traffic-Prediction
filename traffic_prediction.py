# -*- coding: utf-8 -*-
"""Traffic Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_rgfmQrBLG82g2C3pU1pd_T8-ch30OUh
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
def deprecated_function():
  warnings.warn("This function is deprecated and will be removed in a future version.", DeprecationWarning)
#warnings.warn = deprecated_function

data = pd.read_csv("/content/traffic.csv")

data.head(5)

data.columns

data.describe()

data.info()

data.shape

data.isnull().sum()

data.duplicated().sum()

numeric_cols = data.select_dtypes(include = "int")
numeric_cols.corr()

data["DateTime"] = pd.to_datetime(data["DateTime"])

data.dtypes

"""##Feature Construction

Monday = 0
Tuesday = 1
Wednesday = 2
Thursday = 3
Friday = 4
Saturday = 5
Sunday = 6
"""

data["day"] = data['DateTime'].dt.day
data["month"] = data['DateTime'].dt.month
data["year"] = data['DateTime'].dt.year
data["time"] = data["DateTime"].dt.time
data['weekday'] = data['DateTime'].dt.weekday

data

data =data.drop("DateTime", axis=1)

data

data.info()

data.select_dtypes(include = "int").corr()*100

import seaborn as sns
import matplotlib.pyplot as plt

col_dis = ['Junction', 'day', 'month', 'year', 'weekday']

fig, axes = plt.subplots(1, len(col_dis), figsize=(15, 3))
for i,col in enumerate(col_dis):
  sns.countplot(x=col, data=data,ax= axes[i])
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, len(col_dis), figsize=(15, 3))
for i,col in enumerate(col_dis):
  sns.distplot(data[col],ax= axes[i])
plt.tight_layout()
plt.show()

"""##Multivariate Analysis"""

from datetime import time

time_array = data['time']

# Function to generate labels for each hour range
def generate_hour_labels():
    labels = []
    for hour in range(24):
        start_time = f"{hour:02d}:01"
        end_time = f"{hour:02d}:59"
        labels.append(f"{start_time} - {end_time}")
    return labels

# Generate the hourly range labels
hour_labels = generate_hour_labels()

# Function to label time based on hourly ranges
def label_time(t):
    hour = t.hour
    return hour_labels[hour]

# Apply the labeling function to each time in the array
time_labels = np.array([label_time(t) for t in time_array])

print(time_labels)

data['time_label'] = time_labels

data.select_dtypes(include = "int").corr()*100

sns.violinplot(x='Junction', y='Vehicles', data=data)

sns.heatmap(data.select_dtypes(include = "int").corr()*100)

plt.figure(figsize=(40, 20))
sns.boxplot(x='time_label', y='Vehicles', data=data)
plt.title('Box Plot of Value by Category')
plt.show()

from scipy.stats import f_oneway

# Perform ANOVA
categories = data['Vehicles'].unique()
values_by_category = [data[data['Vehicles'] == category]['year'] for category in categories]
anova_result = f_oneway(*values_by_category)

print(f"ANOVA F-value: {anova_result.statistic}, p-value: {anova_result.pvalue}")

plt.figure(figsize=(40, 20))
sns.pointplot(x='Vehicles', y='year', data=data, ci='sd')
plt.title('Point Plot of Mean Value by Category')
plt.show()