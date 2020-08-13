# This is the link to use to get a list of the standards all on one page
## https://shop.bsigroup.com/SearchResults/?q=bs+5266&pg=1&no=100&c=100&t=p

import requests
from bs4 import BeautifulSoup
import re
import os
import argparse
import pdfplumber


parser = argparse.ArgumentParser(description='Extract text from a spec and check the standards')
parser.add_argument('in_filename', help='Input filename (`-` for stdin)')


def return_list_of_standards(standard_name):
    URL = f"https://shop.bsigroup.com/SearchResults/?q={standard_name}&pg=1&no=100&c=100&t=p"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='MainFrame')

    standards_lists = results.find_all('div', class_='resultsInd')
    results_list = []

    for _ in standards_lists:
        title_name = _.find('h2', class_='H2SearchResultsTitle')
        title_status = _.find('span', class_='text12Grey')
        results_list.append(_.text.strip())

    returned_list = []
    for _ in results_list:
        formatted_text = _.replace("  ", "")
        formatted_text = formatted_text.replace("\n\n", "\n")
        formatted_text = formatted_text.replace("\r\n", "")
        formatted_text = formatted_text.replace("\xa0", " ")
        formatted_text = formatted_text.strip('\r')
        output_list = []
        for item in formatted_text.splitlines():
            output_list.append(item)
        output_list[:] = [x for x in output_list if x]
        returned_list.append(output_list)

    return returned_list


def text_search_for_standards(input_text):
    regex = r"(BS|BS |BS EN|EN|EN |ISO|ISO |IEC|IEC |BSRIABG |DW)\d+"

    matches = re.finditer(regex, input_text, re.MULTILINE)
    list_of_standards_in_text = []
    for matchNum, match in enumerate(matches, start=1):
        list_of_standards_in_text.append(match.group())

    return list_of_standards_in_text

def extract_text_from_pdf(in_filename, **input_kwargs):
    with pdfplumber.open(in_filename) as pdf:
        full_text = ""
        pages = pdf.pages
        for i, pg in enumerate(pages):
            text = pages[i].extract_text()
            full_text += text
        #first_page = pdf.pages[0]
        #print(first_page.extract_text())
        #print(full_text)
        return full_text

def main():
    try:
        #Get the file name of the document you wish to search
        args = parser.parse_args()

        sample_text = extract_text_from_pdf(args.in_filename)
        print(sample_text)

        list_of_standards_in_text = text_search_for_standards(sample_text)
        print(list_of_standards_in_text)

        list_of_standards_in_text = list(set(list_of_standards_in_text))

        print("\n\n\n sorted \n\n\n")
        print(list_of_standards_in_text)

        filename_to_write = f"{args.in_filename}.txt"

        with open(filename_to_write, 'w', encoding="utf-8") as standards_review_doc:

            standards_review_doc.write("Summary of Standards:")
            standards_review_doc.write("""

            """)

            for standard_name in list_of_standards_in_text:
                standards_review_doc.write("\n\n=======================================\n\n")
                standards_review_doc.write(standard_name)
                standards_review_doc.write("\n\n\n")
                returned_list = return_list_of_standards(standard_name)
                for item in returned_list:
                    standards_review_doc.write(f"Name: {item[0]}\n")
                    standards_review_doc.write(f"Title: {item[1]}\n")
                    standards_review_doc.write(f"Status: {item[5]} \n\n")


    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
