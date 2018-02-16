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
import pandas as pd


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
    lat, lon = [e.lstrip() for e in re.split(';|/|\uefeff', latlon)[-2:]]
    lon = lon.split('\ufeff')[0]
    wiki_url = row.find_all('td')[1].find_all('a', href=True)[0]['href']
    wiki_url = 'https://wikipedia.org' + wiki_url
    data = {'city': city, 'state': state, 'wiki_url': wiki_url, 'pop': pop,
            'area': area, 'pop_density': density, 'lat': lat, 'lon': lon}
    cities.append(data)

# Restricted to 1 city for testing purposes
for city_data in cities[:1]:
    # Perform google search with wiki_url name + city-data.com
    city_url = city_data['wiki_url'].split('/')[-1]
    query = 'city-data.com' + ' ' + city_url
    url = 'http://www.city-data.com/city/New-York-New-York.html'
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    housing_text = soup.find('section', {'id': 'median-income'}).getText()
    housing_re = 'Estimated median house or condo value in \d{4}: \$\d*[.,]?\d*'
    col_text = soup.find('section', {'id': 'cost-of-living-index'}).getText()
    col_re = '\d*\.\d+|\d+'
    housing = re.findall(housing_re, housing_text)[0].split(': ')[1]
    col = re.findall(col_re, col_text)[1]
    # TODO: Crime
    # section id="crime" tfoot, last td element (for most recent year)
    url = 'http://www.walkscore.com/score/' + city_url
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    imgs_str = ''.join([str(e) for e in soup.find_all('img')])
    walk_src = re.findall('badge/walk/score/\d{1,3}\.svg', imgs_str)[0]
    walk_score = re.split('/|\.', walk_src)[-2]
    bike_src = re.findall('badge/bike/score/\d{1,3}\.svg', imgs_str)[0]
    bike_score = re.split('/|\.', bike_src)[-2]
    transit_src = re.findall('badge/transit/score/\d{1,3}\.svg', imgs_str)[0]
    transit_score = re.split('/|\.', transit_src)[-2]
    city_data['housing_cost'] = housing
    city_data['col_index'] = col
    city_data['walk_score'] = walk_score
    city_data['bike_score'] = bike_score
    city_data['transit_score'] = transit_score
    url = city_data['wiki_url']
    req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})
    climate_table = None
    for table in tables:
        if 'Climate' in table.find_all('tr')[0].find_all('th')[0].getText():
            climate_table = table
            break
    # Feb should be 2nd <td>, Aug 8th, Annual 13th
    if climate_table:
        for row in climate_table.find_all('tr'):
            if len(row.find_all('th')) == 0:
                continue
            row_title = row.find_all('th')[0].getText()
            cells = row.find_all('td')
            if 'Average high' in row_title:
                high = cells[7].getText().split('\n')[0]
            if 'Average low' in row_title:
                low = cells[1].getText().split('\n')[0]
            if 'Average precipitation' in row_title:
                rain = cells[12].getText()
        city_data['avg_feb_low'] = low
        city_data['avg_aug_high'] = high
        city_data['avg_year_precip'] = rain
    climate_table = None
    time.sleep(10)

df = pd.DataFrame(cities)
print(df)
