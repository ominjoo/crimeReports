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
