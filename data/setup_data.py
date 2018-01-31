"""
For each data source, record:
Data name/title
Source URL
Raw source data
Data cleaning code
Cleaned data

Database columns:
City,County,Lat,Lon,Area(sq mi),PropVal,Pop,PopDens,Age,Walk,Crime,CPI,Unempl,
Wages,HighTemp,LowTemp,Precip (days/year),Humid,Pollen

Property values -> https://www.zillow.com/research/data/
Lat -> simplemaps
Lon -> simplemaps
Area -> https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area (and Google)

Climate
https://www.ncdc.noaa.gov/access-data-service/api/v1/data?dataset=global&startDate=2016-01-01&endDate=2016-12-31
Average high temperature
Average low temperature
Annual days of precipitation
Average humidity
Pollen -> http://www.aafa.org/media/Fall-Allergy-Capitals-Report-Dec-2016.pdf

Economic
Consumer Price Index
Unemployment
Average income/wages

Social
Population -> https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
Population density -> Calculated
Median age -> https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=ACS_16_1YR_S0101&prodType=table
Crime rate
Walkability/public transportation/urban density
Race -> https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=ACS_15_5YR_DP05&prodType=table
"""
import csv
import sqlite3


conn = sqlite3.connect('data.db')
curs = conn.cursor()
comm = """
       CREATE TABLE IF NOT EXISTS CitiesData
       (City TEXT,
       County TEXT,
       State TEXT,
       Lat REAL,
       Lon REAL,
       Area REAL,
       PropVal REAL,
       Pop INT,
       PopDens REAL,
       MedianAge REAL,
       WalkScore REAL,
       Crime REAL,
       CPI REAL,
       Unempl REAL,
       Wages REAL,
       HighTemp REAL,
       LowTemp REAL,
       Precip INT,
       Humid REAL,
       Pollen REAL);
       """
curs.execute(comm)

with open('data.csv', 'r') as fid:
    reader = csv.DictReader(fid)
    vals = [(row['City'],
             row['County'],
             row['State'],
             row['Lat'],
             row['Lon'],
             row['Area'],
             row['PropVal'],
             row['Pop'],
             row['PopDens'],
             row['MedianAge'],
             row['WalkScore'],
             row['Crime'],
             row['CPI'],
             row['Unempl'],
             row['Wages'],
             row['HighTemp'],
             row['LowTemp'],
             row['Precip'],
             row['Humid'],
             row['Pollen']) for row in reader]

comm = """
       INSERT INTO CitiesData VALUES
       (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
       """
curs.executemany(comm, vals)

conn.commit()
conn.close()
