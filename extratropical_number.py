import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz  # PyMuPDF library

processed_pdfs = set()

def search_keyword_in_pdf(pdf_url, keyword):
    try:
        response = requests.get(pdf_url, stream=True)
        response.raise_for_status()

        with open('temp.pdf', 'wb') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)

        doc = fitz.open('temp.pdf')

        for page_num in range(doc.page_count):
            page = doc[page_num]
            if keyword.lower() in page.get_text("text").lower():
                return True

    except Exception as e:
        print(f"Error processing {pdf_url}: {e}")

    return False

def search_for_word_in_noaa_pdfs(base_url, keyword):
    found_keyword = False

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a', href=True):
        pdf_url = urljoin(base_url, link['href'])
        if pdf_url.endswith('.pdf') and pdf_url not in processed_pdfs:
            if search_keyword_in_pdf(pdf_url, keyword):
                found_keyword = True
                filename = pdf_url.split("_")[-1].split(".")[0]  # Give me only name pls
                print(f"{filename}")
                processed_pdfs.add(pdf_url)

    if not found_keyword:
        print(f"The keyword '{keyword}' was not found in any PDFs.")

# Example usage:
base_url = "https://www.nhc.noaa.gov/data/tcr/index.php?season=1995&basin=atl"
keyword_to_search = ["became extratropical", " becoming extratropical ", "declared extratropical", "became an extratropical", "remnant extratropical"]

search_for_word_in_noaa_pdfs(base_url, keyword_to_search)

