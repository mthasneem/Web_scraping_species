import requests
from bs4 import BeautifulSoup
import csv

# specify the url and base url
url = "https://doris.ffessm.fr/find/species/"
base_url = "https://doris.ffessm.fr"

# specify the headers to avoid 403 forbidden error
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

# specify the number of pages to scrape
num_pages = 2

# create an empty list to store the results
results = []

# loop through each page and extract the species data
for page in range(1, num_pages+1):
    # calculate the offset for each page
    offset = (page-1)*21
    
    # make a request to the url with the offset
    response = requests.get(f"{url}{offset}", headers=headers)
    
    # parse the html content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # find all the divs with class "specieSearchResult"
    species = soup.findAll('div', class_='specieSearchResult')
    
    # loop through each specie and extract the data
    for specie in species:
        try:
            # get the name and latin name
            name = specie.find('div', class_='padder').a.text.strip()
            latin_name = specie.find('div', class_='padder').em.text.strip()
            
            # get the url of the description and the image
            description_url = specie.find('div', class_='imageCard').a['href']
            image_url = specie.find('div', class_='imageCard').img['src'].strip()
            
            # add the data to the results list
            results.append([name, latin_name, f"{base_url}{description_url}", image_url])
            
        except:
            pass
        
# write the results to a csv file
with open('species.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Latin Name', 'Description URL', 'Image URL'])
    writer.writerows(results)
