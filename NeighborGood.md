# NeighborGood

## What It Is
This is a tool to help you find and choose a neighborhood to live in.

## How to Use It
Go to: <URL>, follow the instructions there.

## Changelog (and Planned Features)
### v1.0
- [] Initial data and proof of concept
### v2.0
- [] More criteria and data
- [] Heatmap of results (Mapbox API)

## Design
Server written in NodeJS. Data aggregation with Python.
cityscraper.py aggregates data from a variety of sources (see Data Sources below) and generates a CSV file with columns for each of the criteria.


## Data Sources
Wikipedia: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
Bureau of Economic Analysis: https://www.bea.gov/regional/downloadzip.cfm
Zillow: https://www.zillow.com/research/data/
Walkscore: https://www.walkscore.com/cities-and-neighborhoods/
National Oceanic and Atmospheric Adminstration: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#data

v1.0
Cities List -> wikipedia.org
Criteria
    Population
        Population -> wikipedia.org
        Population Density -> wikipedia.org
    Cost
        Housing Prices -> zillow.com
        Regional Price Parity -> Bureau of Economic Analysis
    Climate
        Longterm Avg Annual Low -> ncdc.noaa.gov 
        Longterm Avg Annual High -> ncdc.noaa.gov
        Longterm Avg Precipitation Total -> ncdc.noaa.gov
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


## License
Copyright (c) 2017 nobleator

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
