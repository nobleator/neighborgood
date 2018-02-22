# TODO: Integrate zillow data
# TODO: Integrate BEA data
# TODO: Integrate walkscore data (remove API cal)
# TODO: Integrate NOAA API

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import re
import pandas as pd
import numpy as np
from difflib import get_close_matches


class Scraper:
    def __init__(self):
        self.log = []
        self.cities = []
        self.zillow_df = pd.read_csv('zillow_data.csv')
        self.walkscore_df = pd.read_csv('walkscore_data.csv')
        self.bea_rpp_df = pd.read_csv('bea_rpp_data.csv')
        self.populate_cities_list()
        for city in self.cities:
            city = self.get_housing(city)
            city = self.get_walk_score(city)
            city = self.get_rpp(city)
            """try:
                city = self.get_city_data(city)
            except Exception as e:
                self.log_func('Failed to open city-data.com for ' + city['city'] + ' ' + str(e))
            try:
                city = self.get_walk_score(city)
            except Exception as e:
                self.log_func('Failed to open walkscore.com for ' + city['city'] + ' ' + str(e))"""
            try:
                city = self.get_climate(city)
            except Exception as e:
                self.log_func('Failed to access NOAA API for ' + city['city'] + ' ' + str(e))
            self.log_func('Done with ' + city['city'])
            time.sleep(10)
        self.process()

    def log_func(self, text: str=''):
        msg = time.strftime('%X %x %Z') + ': ' + text
        self.log.append(msg)
        print(msg)

    def url_to_soup(self, url: str=''):
        req = Request(url, headers={'User-agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def populate_cities_list(self):
        url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
        soup = self.url_to_soup(url)
        rows = soup.find_all('table', {'class': 'wikitable'})[0].find_all('tr')
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
            self.cities.append(data)
        self.log_func('Gathered list of cities')

    def get_city_data(self, city_data):
        city_data['timestamp'] = time.strftime('%X %x %Z')
        # city_url = city_data['wiki_url'].split('/')[-1]
        # query = 'city-data.com' + ' ' + city_url
        url = 'http://www.city-data.com/city/New-York-New-York.html'
        soup = self.url_to_soup(url)
        housing_text = soup.find('section', {'id': 'median-income'}).getText()
        housing_re = r'Estimated median house or condo value in \d{4}: \$\d*[.,]?\d*'
        col_text = soup.find('section', {'id': 'cost-of-living-index'}).getText()
        col_re = r'\d*\.\d+|\d+'
        housing = re.findall(housing_re, housing_text)[0].split(': ')[1]
        col = re.findall(col_re, col_text)[1]
        city_data['housing_cost'] = housing
        city_data['col_index'] = col
        return city_data
                
    def get_housing(self, city_data):
        region_name = get_close_matches(word=city_data['city'],
                        possibilities=self.zillow_df['RegionName'],
                        cutoff=0.01)[0]
        idx = self.zillow_df.index[self.zillow_df['RegionName'] == region_name]
        price = self.zillow_df.loc[idx]['2017-01'].values[0]
        city_data['housing_cost'] = price
        return city_data
    
    def get_walk_score(self, city_data):
        city_name = get_close_matches(word=city_data['city'],
                        possibilities=self.walkscore_df['City'],
                        cutoff=0.01)[0]
        idx = self.walkscore_df.index[self.walkscore_df['City'] == city_name]
        walk_score = self.walkscore_df.loc[idx]['Walk Score'].values[0]
        bike_score = self.walkscore_df.loc[idx]['Bike Score'].values[0]
        transit_score = self.walkscore_df.loc[idx]['Transit Score'].values[0]
        city_data['walk_score'] = walk_score
        city_data['bike_score'] = bike_score
        city_data['transit_score'] = transit_score
        return city_data

    def get_rpp(self, city_data):
        geo_name = get_close_matches(word=city_data['city'],
                        possibilities=self.bea_rpp_df['GeoName'],
                        cutoff=0.01)[0]
        idx = self.bea_rpp_df.index[(self.bea_rpp_df['GeoName'] == geo_name) &
                                    (self.bea_rpp_df['Description'] == 'RPPs: All items')]
        regional_price_parity = self.bea_rpp_df.loc[idx]['2015'].values[0]
        city_data['rpp'] = regional_price_parity
        return city_data

    def get_climate(self, city_data):
        raise ValueError('Need to implement get_climate()')
    
    def process(self):
        df = pd.DataFrame(self.cities)
        df.to_csv('database_test.csv')
        self.log_func('Wrote DataFrame to database.csv')
        with open('logfile.txt', 'a') as fid:
            fid.write('\n'.join(self.log))


if __name__ == '__main__':
    scraper = Scraper()