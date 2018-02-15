"""
wikipedia.org
Start with https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
Scrape table for population and population density stats
Follow URLs for each city

For each city-specific wiki article:
Measure culture by counting length  of "Culture" section on wikipedia

v1.0
Cities List -> wikipedia.org
Criteria:
    Population
        Population -> wikipedia.org
        Population Density -> wikipedia.org
    Cost
        Housing Prices -> city-data.com
        Cost of Living Index -> city-data.com
    Climate
        Feb Avg Low -> wikipedia.org
        Aug Avg High -> wikipedia.org
        Annual Avg Precipitation Days -> wikipedia.org
    Culture
        Wikipedia Article Length? -> wikipedia.org
        Racial Diversity -> city-data.com
    Transportation
        Walkability -> walkscore.com
        Bikability -> walkscore.com
        Public Transit -> walkscore.com

v2.0
Cities List -> wikipedia.org
Geographic Filtering -> Click on map, sort by distanct from selected point
Criteria:
    Population
        Population -> wikipedia.org
        Population Density -> wikipedia.org
    Cost
        Housing Prices -> city-data.com
        Cost of Living Index -> city-data.com
        Taxes -> State-specific?
    Climate
        Feb Avg Low -> wikipedia.org
        Aug Avg High -> wikipedia.org
        Annual Avg Precipitation Days -> wikipedia.org
    Culture
        Distance to mountains or beaches -> ???
        Wikipedia Article Length? -> wikipedia.org
        Racial Diversity -> city-data.com
    Transportation
        Walkability -> walkscore.com
        Bikability -> walkscore.com
        Public Transit -> walkscore.com
    Economic
        Unemployment Rate -> city-data.com
        Crime Rate -> city-data.com
        Interconnectedness (e.g. number of airports)
        Specific Career Selection -> Select from drop-down menu
"""
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import re


url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
page = urlopen(req).read()
soup = BeautifulSoup(page, 'html.parser')
rows = soup.find_all('table', {'class': 'wikitable'})[0].find_all('tr')
cities = []
for row in rows:
    cells = [e.text.replace(u'\xa0', '').lstrip() for e in row.find_all('td')]
    if len(cells) == 0:
        continue
    _, city, state, pop, _, _, area, _, density, _, latlon = cells
    city = city.rstrip('[0123456789]')
    lat, lon = [e.lstrip() for e in re.split(';|/|\uefef', latlon)[-3:]]
    wiki_url = row.find_all('td')[1].find_all('a', href=True)[0]['href']
    wiki_url = 'https://wikipedia.org' + wiki_url
    cities.append((city, state, wiki_url, pop, area, density, lat, lon))

# Restricted to 1 city for testing purposes
for city_data in cities[:1]:
    # Perform google search with wiki_url name + city-data.com
    city_url = city_data[2].split('/')[-1]
    query = 'city-data.com' + ' ' + city_url
    url = 'http://www.city-data.com/city/New-York-New-York.html'
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    realestate_text = soup.find('section', {'id': 'median-income'}).getText()
    realestate_re = 'Estimated median house or condo value in \d{4}: \$\d*[.,]?\d'
    col_text = soup.find('section', {'id': 'cost-of-living-index'}).getText()
    col_re = '\d{4} cost of living index in .+: \$\d*[.]?\d'
    print(re.findall(realestate_re, realestate_text)[0])
    print(re.findall(col_re, col_text)[0])
    url = 'http://www.walkscore.com/score/' + city_url
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    imgs_str = ''.join([str(e) for e in soup.find_all('img')])
    walk_src = re.findall('badge/walk/score/\d{1,3}\.svg', imgs_str)[0]
    walk_score = re.split('/|\.', walk_src)[-2]
    bike_src = re.findall('badge/bikescore/\d{1,3}\.svg', imgs_str)[0]
    bike_score = re.split('/|\.', walk_src)[-2]
    transit_src = re.findall('badge/transit/score/\d{1,3}\.svg', imgs_str)[0]
    transit_score = re.split('/|\.', walk_src)[-2]
    time.sleep(60)
