# extractor.py

import pdfplumber

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
