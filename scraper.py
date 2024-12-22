import requests
import pdfplumber
import os
import pandas as pd
from bs4 import BeautifulSoup

# URL of the crime logs page
url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/Calls_and_Arrests.asp"

# Send a request to fetch the content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the <select> element and get all options (pdf links)
dropdown = soup.find("select")
options = dropdown.find_all("option")

# Collect all available PDF links
pdf_links = []
base_url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/"
for option in options[1:]:  # Skipping the first option (typically not a report)
    pdf_link = option['value']
    pdf_links.append(base_url + pdf_link)

# Function to extract crime data from each PDF
def extract_crime_data(pdf_filename):
    crime_data = []
    with pdfplumber.open(pdf_filename) as pdf:
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            text = page.extract_text()

            if text:  # Check if there is text on the page
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    line = line.strip()

                    # Capture crime details after "CRIME AND FIRE LOG/MEDIA BULLETIN"
                    if "CRIME AND FIRE LOG/MEDIA BULLETIN" in line:
                        if i + 2 < len(lines):  # Crime type line
                            crime_type = lines[i + 2].strip()
                        if i + 3 < len(lines):  # Location line
                            location = lines[i + 3].strip()
                        if i + 7 < len(lines):  # Time line
                            time_line = lines[i + 7].strip()
                            if "Time Occurred" in time_line:
                                time = time_line.split("Time Occurred")[-1].strip()

                                crime_data.append({'crime_type': crime_type, 'location': location, 'time': time})
                    
                    # If "Disposition" found, capture the following details
                    if line.startswith("Disposition:"):
                        if i + 1 < len(lines):  # Crime type line
                            crime_type = lines[i + 1].strip()
                        if i + 2 < len(lines):  # Location line
                            location = lines[i + 2].strip()
                        if i + 6 < len(lines):  # Time line
                            time_line = lines[i + 6].strip()
                            if "Time Occurred" in time_line:
                                time = time_line.split("Time Occurred")[-1].strip()

                                crime_data.append({'crime_type': crime_type, 'location': location, 'time': time})

    return crime_data

# Collect all crime data from each PDF
all_crime_data = []

# Download and process each PDF
for pdf_link in pdf_links:
    pdf_filename = pdf_link.split("/")[-1]

    # Check if the PDF already exists locally
    if os.path.exists(pdf_filename):
        print(f"Skipping {pdf_filename}, already downloaded.")
    else:
        # Download the PDF if not already present
        pdf_response = requests.get(pdf_link)
        with open(pdf_filename, "wb") as f:
            f.write(pdf_response.content)
        print(f"Downloaded {pdf_filename}")

    # Process the PDF and extract crime data
    crime_data = extract_crime_data(pdf_filename)
    all_crime_data.extend(crime_data)

# Convert the collected data into a DataFrame
df = pd.DataFrame(all_crime_data)
df.to_csv("ucsd_crime_data.csv", index=False)
print(df.isnull().sum())
