# This is the link to use to get a list of the standards all on one page
## https://shop.bsigroup.com/SearchResults/?q=bs+5266&pg=1&no=100&c=100&t=p

import requests
from bs4 import BeautifulSoup


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


def main():
    standard_name = input("Input name of standard: ")
    returned_list = return_list_of_standards(standard_name)
    for item in returned_list:
        print(f"Name: {item[0]}")
        print(f"Title: {item[1]}")
        print(f"Status: {item[5]} \n")


if __name__ == '__main__':
    main()
