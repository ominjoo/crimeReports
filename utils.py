# utils.py

import os
import requests

def download_pdf(pdf_link, pdf_filename):
    # Check if the PDF already exists locally
    if os.path.exists(pdf_filename):
        print(f"Skipping {pdf_filename}, already downloaded.")
    else:
        # Download the PDF if not already present
        pdf_response = requests.get(pdf_link)
        with open(pdf_filename, "wb") as f:
            f.write(pdf_response.content)
        print(f"Downloaded {pdf_filename}")


categories = {
    'Theft and Damage': ['theft', 'petty', 'burglary', 'shoplifting', 'stealing', 'extortion', 'robbery', 'fraud', 'property', 'vandalism', 'damage', 'missing vehicle', 'tampering'],
    'Violent': ['violence', 'assault', 'battery', 'sexual', 'weapons', 'threaten', 'threat', 'hate', 'terrorize', 'rape'],
    'Traffic' : ['traffic', 'signal light', 'hit and run', 'hit & run', 'pedestrian', 'reckless driving', 'drunk driving', 'traffic violation', 'collision', 'parking', 'ticket', 'impound'],
    'Disturbance': ['disturbance', 'camping', 'solicitng', 'loitering', 'noise', 'alarm', 'suspicious', 'trespass', 'harassing', 'annoying', 'fire', 'threatening', 'quiet hours', 'dispute', 'stay away'],
    'Drugs': ['drug','possession', 'intoxication', 'trafficking', 'paraphernalia', 'marijuana', 'alcohol', 'drunk'],
    'Welfare': ['welfare', 'injury', 'medical', 'suicide', 'Psych', 'missing person', 'Check', 'mental', 'health'],
    'Non-Emergent Call or Report': ['Incomplete/Accidental', 'Incomplete/ Accidental', 'Incomplete / Accidental', 'Information', 'report']
}

# Function to categorize crimes based on keywords
def categorize_crime(crime):
    for category, keywords in categories.items():
        if any(keyword.lower() in crime.lower() for keyword in keywords):
            return category
    return 'Other'  # Return 'Other' if no category matches