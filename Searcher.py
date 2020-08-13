# This is the link to use to get a list of the standards all on one page
## https://shop.bsigroup.com/SearchResults/?q=bs+5266&pg=1&no=100&c=100&t=p

import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
import os

sample_text = """
The services will require to be heavily isolated from the fabric of the building to avoid the 
transmission of noise between the interior and exterior and between internal spaces. Hangers and 
vibration isolation mountings shall be a contractor design item to achieve the criteria defined by 
Level acoustics. 
The smoke ventilation system shall be a specialist contractor design and installation to achieve the 
requirements of BS EN 12101, the documents show the design intent and the WSP fire report 
provides the necessary performance criteria that the smoke control specialist shall develop into a 
full scheme. 
Calculation of all feed and expansion and the selection of anchor points and expansion joints shall be 
the responsibility of the specialist supplier. Care shall be taken that the design of the system does 
not compromise the acoustic performance or the structural requirement for movement joints. 
The BMS shall be designed by a specialist developing the description of operations into a full points 
schedule with all the necessary sensors, actuators, control algorithms, software engineering, field 
wiring and containment for the controls to form a fully functioning system that will enable the 
building to be operated in the most energy efficient manner.  
Water treatment and chemical flushing and cleaning of the distribution systems shall be undertaken 
by a specialist  BS7671 BS EN 60309 BS 8266 ISO53 ISO 12323423 ISO1 EN54
"""

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
    regex = r"(BS|BS |BS EN|EN|EN |ISO|ISO )\d+"

    matches = re.finditer(regex, input_text, re.MULTILINE)
    list_of_standards_in_text = []
    for matchNum, match in enumerate(matches, start=1):
        list_of_standards_in_text.append(match.group())

    return list_of_standards_in_text


def main():
    try:
        list_of_standards_in_text = text_search_for_standards(sample_text)
        print(list_of_standards_in_text)

        print("Summary of Standards:")
        print("""

        """)

        for standard_name in list_of_standards_in_text:
            print("=======================================")
            print(standard_name)
            print("""

            """)
            returned_list = return_list_of_standards(standard_name)
            for item in returned_list:
                print(f"Name: {item[0]}")
                print(f"Title: {item[1]}")
                print(f"Status: {item[5]} \n")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
