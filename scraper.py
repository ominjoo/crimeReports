import requests
import pdfplumber
from bs4 import BeautifulSoup

# URL of the crime logs page
url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/Calls_and_Arrests.asp"

# Send a request to fetch the content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the <select> element
dropdown = soup.find("select")
options = dropdown.find_all("option")

# Get the most recent PDF link from the first <option>
recent_option = options[1];

recent_link = recent_option['value']  # Assuming this is the link to the PDF

# Print the link to confirm

base_url = "https://www.police.ucsd.edu/docs/reports/CallsandArrests/"
full_pdf_link = base_url + recent_link
print(f'Most Recent PDF Link: {full_pdf_link}')
pdf_response = requests.get(full_pdf_link)
pdf_filename = recent_link.split("/")[-1]
if pdf_response.status_code == 200:
    pdf_filename = recent_link.split("/")[-1]  # Extract the filename
    with open(pdf_filename, "wb") as f:
        f.write(pdf_response.content)
    print(f"PDF '{pdf_filename}' downloaded successfully.")
else:
    print("Failed to download PDF. Status code:", pdf_response.status_code)


# Function to extract crime types and their locations
def extract_crime_data(pdf_filename):
    with pdfplumber.open(pdf_filename) as pdf:
        with pdfplumber.open(pdf_filename) as pdf:
            for page_number in range(len(pdf.pages)):
                page = pdf.pages[page_number]
                text = page.extract_text()
                if text:  # Check if there is text on the page
                    lines = text.split('\n')

                    for i, line in enumerate(lines):
                        line = line.strip()

                        # Capture the first crime two lines after "CRIME AND FIRE LOG/MEDIA BULLETIN"
                        if "CRIME AND FIRE LOG/MEDIA BULLETIN" in line:
                            if i + 2 < len(lines):  # Check two lines after
                                crime_type = lines[i + 2].strip()  # Capture crime type
                                print(f'First Crime Type: {crime_type}')
                            if i + 3 < len(lines):  # Check the line after the crime type
                                location = lines[i + 3].strip()  # Capture location
                                print(f'Location: {location}')
                            print('---')
                        # If we find "Disposition", capture the next two lines
                        if line.startswith("Disposition:"):
                            if i + 1 < len(lines):  # Next line for crime type
                                crime_type = lines[i + 1].strip()
                            if i + 2 < len(lines):  # Next line for location
                                location = lines[i + 2].strip()
                                
                            print(f'Crime Type: {crime_type}')
                            print(f'Location: {location}')
                            print('---')

# Call the function
extract_crime_data(pdf_filename)