import random
from googleapiclient.discovery import build
import requests
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

API_KEY = 'something'
SEARCH_ENGINE_ID = 'something'


# https://www.thepythoncode.com/article/use-google-custom-search-engine-api-in-python
def web_scrape_google(search_query):
    # the search query you want
    query = search_query
    # using the first page
    page = 1
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

    # make the API request
    data = requests.get(url).json()

    # get the result items
    search_items = data.get("items")
    # iterate over 10 results found

    url_list = []
    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        # get the page title
        title = search_item.get("title")
        # page snippet
        snippet = search_item.get("snippet")
        # alternatively, you can get the HTML snippet (bolded keywords)
        html_snippet = search_item.get("htmlSnippet")
        # extract the page url
        link = search_item.get("link")
        url_list.append(link)
        # print the results
        print("=" * 10, f"Result #{i + start - 1}", "=" * 10)
        print("Title:", title)
        print("Description:", snippet)
        print("Long description:", long_description)
        print("URL:", link, "\n")

        file_path = f"Query_URL/Development_Scalability_Start_Url/{query}.txt"
        with open(file_path, 'w') as file:
            # Write each URL to a new line in the file
            for url in url_list:
                file.write(url + '\n')


user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def web_scrape_page():

    url = 'https://www.datamation.com/cloud/saas-companies/'
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")

    div_id = "tdi_66"
    div_class = "tdb-block-inner td-fix-index"
    item = "h4"
    item_class = "ez-toc-section"

    results = soup.find(id=div_id)
    elements = results.find_all("div", class_=div_class)

    full_list = []
    for i, element in enumerate(elements):
        found_element = element.find_all(item)
        full_list += [x.text.strip() for x in found_element]

    file_path = f"Query_URL/saas_companies.txt"
    with open(file_path, 'w') as file:
        for t in full_list:
            file.write(t + '\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = 'Query_URL/scalability_companies.txt'  # Replace with the actual file path
    with open(file_path, 'r') as file:
        company_list = file.read().splitlines()

    file_path = 'Query_URL/development_scalability_synonyms.txt'  # Replace with the actual file path
    with open(file_path, 'r') as file:
        synonyms_list = file.read().splitlines()

    file_path = 'Query_URL/documentation_scalability_queries.txt'  # Replace with the actual file path
    with open(file_path, 'r') as file:
        documentation_queries = file.read().splitlines()

    j = 0
    # for q in documentation_queries:
    #     if j >= 22:
    #         break
    for i in synonyms_list:
        query = random.choice(company_list)+" "+random.choice(documentation_queries)+"+for+"+i
        query = query.lstrip()
        query = query.replace(" ", "+")
        web_scrape_google(query)
        print(query)
        j += 1
    print(j)
    # for q in synonyms_list:
    #     for i in range(10):
    #         query = random.choice(company_list)+"+software+"+q
    #         query = query.replace(" ", "+")
    #         print(query)
    #         web_scrape_google(query)


    # web_scrape_google("grammarly+software+purpose")
    #web_scrape_page()
