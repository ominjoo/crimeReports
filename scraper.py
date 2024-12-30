# scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_pdf_links(url):
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

    return pdf_links
