from bs4 import BeautifulSoup
import sqlite3, datetime, requests, re, json, difflib

class Aggregator:
	def __init__(self):
		"""
		Table schema
		zip code, county, city, state
		"""
		self.conn = sqlite3.connect('test.db')
		self.zip_codes = ['22201']#, '80014', '94016']
		self.states = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID',
					'IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT',
					'NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
					'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
		self.state_to_state_id = {self.states[i]: str(i+1) for i in range(0,len(self.states))}
		self.valid_agencies = []
		self.agency_to_crime_cross_id = {}
		self.zip_to_state = {}
		self.zip_to_county = {}
		self.get_zip_to_county()
		# Table for pollen data
		self.conn.execute("""CREATE TABLE IF NOT EXISTS pollen 
								(zip_code TEXT, 
								pollen TEXT, 
								access_date TEXT)""")
		# Table for walkability data
		self.conn.execute("""CREATE TABLE IF NOT EXISTS walkability 
								(zip_code TEXT, 
								walk_score TEXT, 
								access_date TEXT)""")
		# Table for unemployment data
		self.conn.execute("""CREATE TABLE IF NOT EXISTS unemployment 
								(zip_code TEXT, 
								unemployment_rate TEXT, 
								access_date TEXT)""")
								
	def scrape_pollen(self):
		"""
		Scrape www.pollen.com for index ratings for zip codes and store in database
		Table schema
		zip_code TEXT, pollen TEXT, access_date TEXT
		"""
		url_form = 'https://www.pollen.com/api/forecast/current/pollen/'
		insert_form = 'INSERT INTO pollen VALUES ("{0}", "{1}", "{2}")'
		for zip_code in self.zip_codes:
			pollen_rating = -1
			headers = {'Host': 'www.pollen.com',
					'Accept': 'application/json, text/plain, */*',
					'Referer': 'https://www.pollen.com/forecast/current/pollen/'+zip_code}
			response = requests.get(url_form + zip_code, headers=headers)
			pollen_periods = response.json()[u'Location'][u'periods']
			for period in pollen_periods:
				if period[u'Type'] == u'Today':
					pollen_rating = period[u'Index']
			access_date = datetime.datetime.now()
			command = insert_form.format(zip_code, pollen_rating, access_date)
			self.conn.execute(command)		
		
	def scrape_walkability(self):
		"""
		Scrape www.walkscore.com for walkability ratings for zip codes and store in
		database
		Table schema
		zip_code TEXT, walkability TEXT, access_date TEXT
		"""
		# Convert zip code to /state/county/zip
		url_form = 'https://www.walkscore.com/'
		insert_form = 'INSERT INTO pollen VALUES ("{0}", "{1}", "{2}")'
		for zip_code in self.zip_codes:
			state = 'VA'
			county = 'Arlington'
			url = url_form + state + '/' + county + '/' + zip_code
			response = requests.get(url)
			content = response.content
			soup = BeautifulSoup(content, 'html.parser')
			# Return regex matching /\d*\.svg"
			pattern = re.compile('/\d*\.svg"')
			match = pattern.search(str(soup))
			walk_score = match.group()[1:-5]
			access_date = datetime.datetime.now()
			command = insert_form.format(zip_code, walk_score, access_date)
			self.conn.execute(command)
		
	def get_zip_to_county(self):
		"""
		Convert zip code to county+state
		# Use if getzip.com stops working?
		# zipcodeapi.com -> reutrns 'API key not found'
		api_key = 'autK2v5z10VEXQjONMOW9Bzs3TRzzcWJGpuJVAiXBeBz5VnSHcOQOoiRhaqRnnB3'
		zip_code = '22201'
		url_form = 'https://www.zipcodeapi.com/rest/{0}/info.json/{1}/degrees'
		url = url_form.format(api_key, zip_code)
		print(url)
		#headers = {'Content-type': 'application/json'}
		#payload = json.dumps({"seriesid": series,"startyear":"2016", "endyear":"2016"})
		response = requests.get(url)
		json_data = json.loads(response.text)
		print(json_data)
		"""
		# GET request -> Convert to POST request?
		url_form = 'http://www.getzips.com/cgi-bin/ziplook.exe?What=1&Zip={0}&Submit=Look+It+Up'
		for zip_code in self.zip_codes:
			url = url_form.format(zip_code)
			response = requests.get(url)
			content = response.content
			soup = BeautifulSoup(content, 'html.parser')
			table_elements = soup.body.hr.find_all('td')
			city_state = str(table_elements[5].contents[0].get_text())
			state = city_state.split()[-1]
			county = str(table_elements[6].contents[0].get_text())
			self.zip_to_county[zip_code] = county+' County, '+state
			self.zip_to_state[zip_code] = state
			
	def scrape_unemployment(self):
		"""
		Access the Bureau of Labor Statistics' public API and store in database
		https://www.bls.gov/lau/lausad.htm#sr
		https://www.bls.gov/help/hlpforma.htm#LA
		
		Table schema
		zip_code TEXT, unemployment_rate TEXT, access_date TEXT
		"""
		# Get BLS area codes for counties
		county_to_bls = {}
		url = 'https://download.bls.gov/pub/time.series/la/la.area'
		response = requests.get(url)
		raw_content = response.content
		parsed_content = raw_content.split('\n')
		for line in parsed_content:
			if line[:1] == 'F':
				line_list = line.split('\t')
				series_id = line_list[1][2:]
				county_state = line_list[2]
				county_to_bls[county_state] = series_id
		
		"""
		# Series ID example: 'LAUCN281070000000003'
		# Local Area data
		series_id = 'LA'
		# U: Unadjusted for season
		# S: Seasonally adjusted
		series_id += 'U'
		# County area type
		series_id += 'CN'
		# County area code
		series_id += ''
		# Measure type
		# 06: Labor force
		# 05: Employment
		# 04: Unemployment
		# 03: Unemployment rate
		series_id += '03'
		"""
		series = []
		series_id_form = 'LAUCN{}03'
		for zip_code in self.zip_codes:
			# Convert zip code to county+state
			county_state = self.zip_to_county[zip_code]
			# Convert county+state to BLS area code
			bls_area_code = county_to_bls[county_state]
			series.append(series_id_form.format(bls_area_code))
		
		# Ping API and store results
		url = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
		insert_form = 'INSERT INTO unemployment VALUES ("{0}", "{1}", "{2}")'
		headers = {'Content-type': 'application/json'}
		payload = json.dumps({"seriesid": series,"startyear":"2016", "endyear":"2016"})
		response = requests.post(url, data=payload, headers=headers)
		json_data = json.loads(response.text)
		for series_id in json_data[u'Results'][u'series']:
			annual_sum = 0
			for month in series_id[u'data']:
				print(float(month[u'value']))
				annual_sum += float(month[u'value'])
			annual_avg = annual_sum/12
			access_date = datetime.datetime.now()
			command = insert_form.format(zip_code, annual_avg, access_date)
			self.conn.execute(command)		
		
	def get_crime_cross_id(self):
		url = 'https://www.ucrdatatool.gov/Search/Crime/Local/OneYearofDataStepTwo.cfm'
		headers = {'DNT': '1',
					'Content-Type': 'application/x-www-form-urlencoded',
					'Referer': 'https://www.ucrdatatool.gov/Search/Crime/Local/OneYearofData.cfm',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Origin': 'https://www.ucrdatatool.gov'}
		for state in self.states:
			state_id = self.state_to_state_id[state]
			payload = {'StateId': state_id,
						'DataType': '0',
						'BJSPopulationGroupId': '',
						'NextPage': 'Next'}
			response = requests.post(url, headers=headers, data=payload)
			content = response.content
			soup = BeautifulSoup(content, 'html.parser')
			agencies = soup.find_all('select', {'id': 'agencies'})[0].find_all('option')
			dup_count = 0
			for agency in agencies:
				crime_cross_id = agency['value']
				agency_name = str(agency.get_text()) + ', ' + state
				self.valid_agencies.append(agency.get_text())
				self.agency_to_crime_cross_id[agency_name] = crime_cross_id
		
	def scrape_crime_rate(self):
		url = 'https://www.ucrdatatool.gov/Search/Crime/Local/RunCrimeOneYearofData.cfm'
		headers = {'DNT': '1',
					'Content-Type': 'application/x-www-form-urlencoded',
					'Referer': 'https://www.ucrdatatool.gov/Search/Crime/Local/OneYearofDataStepTwo.cfm',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Origin': 'https://www.ucrdatatool.gov'}
		"""
		StateID: Alphabetical numbering of states (AL = 1, AK = 2, etc.)
		CrimeCrossID: Agency-specific crime tracking ID
		DataType: 3 = Violent crime rates, 4 = Property crime rates
		"""
		table_data = {}
		
		for zip_code in self.zip_codes:
			state = self.zip_to_state[zip_code]
			state_id = self.state_to_state_id[state]
			county = self.zip_to_county[zip_code]
			possible_agency = str(county) + 'Police Department'
			agency = difflib.get_close_matches(possible_agency, self.valid_agencies)[0]
			#agency = self.zip_code_to_agency[zip_code]
			agency_and_state = agency + ', ' + state
			crime_cross_id = self.agency_to_crime_cross_id[agency_and_state]
			payload = {'StateId': state_id,
						'CrimeCrossId': crime_cross_id,
						'BJSPopulationGroupId': '',
						'DataType': '3',
						'YearStart': '2014',
						'NextPage': 'Get Table'}
			response = requests.post(url, headers=headers, data=payload)
			content = response.content
			soup = BeautifulSoup(content, 'html.parser')
			raw_table_elements = soup.body.find_all('td')
			agency = None
			state = None
			violent_crime_rate = None
			murder_rate = None
			robbery_rate = None
			aggravated_assault_rate = None
			for element in raw_table_elements:
				if 'headers="agency"' in str(element):
					agency = str(element.get_text())
				if 'headers="state"' in str(element):
					state = str(element.get_text())
				if 'headers="rate vcrime2 vctot2"' in str(element):
					violent_crime_rate = str(element.get_text()).strip()
				if 'headers="rate vcrime2 murd2"' in str(element):
					murder_rate = str(element.get_text()).strip()
				if 'headers="rate vcrime2 rob2"' in str(element):
					robbery_rate = str(element.get_text()).strip()
				if 'headers="rate vcrime2 aggr2"' in str(element):
					aggravated_assault_rate = str(element.get_text()).strip()
			table_data[agency] = {'state': state,
									'violent crime rate': violent_crime_rate,
									'murder rate': murder_rate,
									'robbery rate': robbery_rate,
									'aggravated assault rate': aggravated_assault_rate}
		print(table_data)
	
if __name__ == '__main__':
	agg = Aggregator()
	#agg.scrape_pollen()
	#agg.scrape_walkability()
	#agg.scrape_unemployment()
	agg.get_crime_cross_id()
	agg.scrape_crime_rate()
	"""
	agg.conn.commit()
	cur = agg.conn.cursor()
	print('pollen table')
	for row in cur.execute('SELECT * FROM pollen'):
		print(row)
	print('walkability table')
	for row in cur.execute('SELECT * FROM walkability'):
		print(row)
	print('unemployment table')
	for row in cur.execute('SELECT * FROM unemployment'):
		print(row)	
	"""
	agg.conn.close()
	
	
	