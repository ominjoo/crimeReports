import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def clean_data(df):

    # Remove rows where 'time', 'location', or 'crime_type' is "Unknown"
    df = df[(df['time'] != 'Unknown') & (df['location'] != 'Unknown') & (df['crime_type'] != 'Unknown')]

    # Encode 'crime_type' as labels (for prediction)
    label_encoder = LabelEncoder()
    df['crime_type_encoded'] = label_encoder.fit_transform(df['crime_type'])

    # Frequency Encoding for 'location' column
    df['location_frequency'] = df['location'].map(df['location'].value_counts())
    
    # Convert time to hour of the day (24-hour format)
    df['time'] = df['time'].apply(lambda x: extract_hour(x))

    
    df.dropna(inplace=True)

    return df

def extract_hour(time):
    try:
        # Convert to datetime and extract hour
        time_obj = pd.to_datetime(time, format='%I:%M %p')
        return time_obj.hour
    except Exception as e:
        # If conversion fails (e.g., 'Unknown'), return NaN or a default value
        return np.nan