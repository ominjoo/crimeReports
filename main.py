import os
import pandas as pd
from scraper import scrape_pdf_links
from extractor import extract_crime_data
from utils import download_pdf
from cleaning import clean_data  # Import the data cleaning function
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# URL of the crime logs page
url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/Calls_and_Arrests.asp"

# Get the list of PDF links
pdf_links = scrape_pdf_links(url)

# Collect all crime data from each PDF
all_crime_data = []

# Download and process each PDF
for pdf_link in pdf_links:
    pdf_filename = pdf_link.split("/")[-1]

    # Download the PDF
    download_pdf(pdf_link, pdf_filename)

    # Process the PDF and extract crime data
    crime_data = extract_crime_data(pdf_filename)
    all_crime_data.extend(crime_data)

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_crime_data)

# Save the DataFrame to a CSV file
df.to_csv("ucsd_crime_data.csv", index=False)

print("Crime data saved to ucsd_crime_data.csv")

print("Cleaning the data...")
df_cleaned = clean_data(df)
df_cleaned = df_cleaned.drop(['crime_type', 'location'], axis=1)
df_cleaned.to_csv("ucsd_crime_data_encoded.csv", index=False)