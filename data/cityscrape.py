from bs4 import BeautifulSoup
import requests
import json
import time
import re
import pandas as pd
import numpy as np
from difflib import get_close_matches
try:
    import config
except ModuleNotFoundError as e:
    print('config.py file not found.')


class Scraper:
    def __init__(self):
        self.noaa_token = config.CONFIG['NOAA_TOKEN']
        self.log_list = []
        self.cities = []
        self.cityids = {}
        self.zillow_df = pd.read_csv('zillow_data.csv')
        self.walkscore_df = pd.read_csv('walkscore_data.csv')
        self.bea_rpp_df = pd.read_csv('bea_rpp_data.csv')
        self.populate_cities_list()
        #self.validate_cityids()
        self.get_cityids()
        for city in self.cities:
            try:
                self.get_housing(city)
            except Exception as e:
                self.log('Failed to get Zillow data for ' + city['city'] + ' ' + str(e))
            try:
                self.get_walk_score(city)
            except Exception as e:
                self.log('Failed to Walk Score data for ' + city['city'] + ' ' + str(e))
            try:
                self.get_rpp(city)
            except Exception as e:
                self.log('Failed to get BEA data for ' + city['city'] + ' ' + str(e))
            try:
                self.get_noaa(city)
            except Exception as e:
                self.log('Failed to access NOAA API for ' + city['city'] + ' ' + str(e))
            self.log('Done with ' + city['city'])
            time.sleep(10)
        self.process()

    def log(self, text: str=''):
        msg = time.strftime('%X %x %Z') + ': ' + text
        self.log_list.append(msg)
        print(msg)

    def url_to_soup(self, url: str=''):
        page = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
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
        self.log('Gathered list of cities')
                
    def validate_cityids(self):
        """
        There are 845 US city IDs for US cities, starting at index 1069
        (when sorted ascending by cityid). This may change depending on how 
        NOAA handles updates.
        This method serves to verify the information above, which should not
        need to occur on every datacall.
        """
        raise NotImplementedError('Need to implement validate_cityids()')

    def get_cityids(self):
        # Convert API response to {city: cityid}
        url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?'
        params = ['locationcategoryid=CITY', 'sortfield=id', 'sortorder=asc',
                  'limit=845', 'offset=1069']
        url += '&'.join(params)
        res = requests.get(url=url, headers={'token': self.noaa_token})
        cityids = json.loads(res.text)['results']
        for city in cityids:
            self.cityids[city['name']] = city['id']
    
    def get_housing(self, city_data: dict={}):
        region_name = get_close_matches(word=city_data['city'],
                        possibilities=self.zillow_df['RegionName'],
                        cutoff=0.01)[0]
        idx = self.zillow_df.index[self.zillow_df['RegionName'] == region_name]
        price = self.zillow_df.loc[idx]['2017-01'].values[0]
        city_data['housing_cost'] = price
    
    def get_walk_score(self, city_data: dict={}):
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

    def get_rpp(self, city_data: dict={}):
        geo_name = get_close_matches(word=city_data['city'],
                        possibilities=self.bea_rpp_df['GeoName'],
                        cutoff=0.01)[0]
        idx = self.bea_rpp_df.index[(self.bea_rpp_df['GeoName'] == geo_name) &
                                    (self.bea_rpp_df['Description'] == 'RPPs: All items')]
        regional_price_parity = self.bea_rpp_df.loc[idx]['2015'].values[0]
        city_data['rpp'] = regional_price_parity

    def get_noaa(self, city_data: dict={}):
        """
        Sets multiple criteria
        Long-term averages of annual maximum temperature, ANN-TMAX-NORMAL
        Long-term averages of annual minimum temperature, ANN-TMIN-NORMAL
        Long-term averages of annual precipitation totals, ANN-PRCP-NORMAL
        """
        location_id = self.cityids[get_close_matches(word=city_data['city'],
                                    possibilities=[*self.cityids],
                                    cutoff=0.01)[0]]
        # datatypes = ['ANN-PRCP-NORMAL', 'ANN-TMAX-NORMAL', 'ANN-TMIN-NORMAL']
        dataset = 'NORMAL_ANN'
        for offset in range(0, 10001, 1000):
            url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?'
            params = ['datasetid=' + dataset, 'locationid=' + location_id,
                      'units=standard', 'startdate=2010-01-01',
                      'enddate=2010-12-31', 'limit=1000',
                      'offset=' + str(offset)]
            url += '&'.join(params)
            res = requests.get(url=url, headers={'token': self.noaa_token})
            if not res.ok or not json.loads(res.text):
                #print('failed request', res.reason, res.text)
                #print(url)
                time.sleep(0.5)
                continue
            for record in json.loads(res.text)['results']:
                if record['datatype'] == 'ANN-PRCP-NORMAL':
                    city_data['precipitation'] = record['value']
                if record['datatype'] == 'ANN-TMAX-NORMAL':
                    city_data['max_temp'] = record['value']
                if record['datatype'] == 'ANN-TMIN-NORMAL':
                    city_data['min_temp'] = record['value']
            time.sleep(0.5)
    
    def process(self):
        df = pd.DataFrame(self.cities)
        df.to_csv('database.csv', index=False)
        self.log('Wrote DataFrame to database.csv')
        with open('logfile.txt', 'a') as fid:
            fid.write('\n'.join(self.log_list))


if __name__ == '__main__':
    try:
        scraper = Scraper()
    except ModuleNotFoundError:
        print('Configuration not set, exiting.')
