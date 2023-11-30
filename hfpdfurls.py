import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz  # PyMuPDF library

processed_pdfs = set()

def search_keywords_in_pdf(pdf_url, keywords):
    try:
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()

        with open('temp.pdf', 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        doc = fitz.open('temp.pdf')

        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text("text").lower()

            if any(keyword.lower() in page_text for keyword in keywords):
                return True

    except Exception as e:
        print(f"Error processing {pdf_url}: {e}")

    return False

def search_for_keywords_in_noaa_pdfs(base_url, keywords):
    found_keywords = False

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a', href=True):
        pdf_url = urljoin(base_url, link['href'])
        if pdf_url.endswith('.pdf') and pdf_url not in processed_pdfs:
            if search_keywords_in_pdf(pdf_url, keywords):
                found_keywords = True
                filename = pdf_url.split("_")[-1].split(".pdf")[0]  # Extracting the filename
                print(f"{filename}")
                processed_pdfs.add(pdf_url)

    if not found_keywords:
        print("None of the keywords were found in any PDFs.")

# Example usage:
base_url = "https://www.nhc.noaa.gov/data/tcr/index.php?season=2023&basin=atl"
keywords_to_search = ["extratropical storm", "became extratropical", " becoming extratropical", 
                      "declared extratropical", "became an extratropical", "remnant extratropical",
                      "extratropical remnants", "extratropical system", "extratropical to"]

search_for_keywords_in_noaa_pdfs(base_url, keywords_to_search)
