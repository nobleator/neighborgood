# NeighborGood

## What It Is
This is a tool to help you find and choose a neighborhood to live in.

## How to Use It
Go to: https://better-neighborgood.herokuapp.com, follow the instructions there.

## Changelog (and Planned Features)
### v1.0
- [x] Initial data and proof of concept
### v2.0
- [] More criteria and data
- [] Heatmap of results (Mapbox API)

## Problem Statement and Design
### Problem Statement
Every year around early March I start sneezing, and I don’t really stop until July. This has led me to dream of moving to another, less pollenated area of the country. But where? Santa Barbara has nice weather, New York City has robust public transportation, and Denver has beautiful vistas. How do I figure out which city would have just the right elements for me and my tastes? Thinking back to my undergraduate days, this sounded like a classic decision analysis problem. Reviewing my class notes, I decided to implement a version of the <a>Analytic Hierarchy Process</a>.
### Design
The first step was collecting data. I spent many hours trawling though US Census data, but ultimately ended up starting with <a>Wikipedia’s list of US cities by population</a>. I used Python’s BeautifulSoup to scrape the table on that page and generate my initial Pandas DataFrame with city, state, population, population density, and latitude/longitude data. I also found some pre-made datasets from the <a>Bureau of Economic Analysis</a> for Regional Price Parities and from <a>Zillow for home sales</a>. I had one more scraping effort as well, as I found a site published by <a>Walk Score listing scores for US cities</a>. I realized that it was much easier to simply copy the text on that page and save to a CSV (rather than using BeautifulSoup), so that’s what I did. The last part of data aggregation involved using the <a>National Oceanic and Atmospheric Administration (NOAA) National Centers for Environmental Information (NCEI) (formerly the National Climatic Data Center (NCDC)) API</a>. The final DataFrame was then exported to a CSV file and then that CSV file was copied into my PostgreSQL databases (one local and one remote on <a>Heroku</a>, my selected hosting provider).

Next up is the server. I decided to experiment with <a>NodeJS + Express</a> for this project. I wanted to create a single page application where the data was loaded into the page via AJAX calls. At the same time, one of the purposes of this effort was to learn web development. I looked at frameworks and templating engines, but I was unsatisfied with how much of the work became a black box, so I decided to lean away from frameworks and implement as much in pure Javascript as I could. I ended up writing three routes; one for the base HTML page and two more for AJAX calls. The first AJAX route would query the database to populate the list of possible criteria, while the second route was a bit more complicated. The client POSTed a list of selected criteria and “weights” (pairwise comparisons between related criteria), which the server then used to generate matrices and calculate weights. These weights are multiplied by the value <mark>(should be converted to rank and rank used)</mark> for that criteria, returned from the database, to calculate the final utility for that criteria. All the cities are sorted to only retrieve the top ten results, which are sent back to the client (along with cost).

Finally we have the client. It is very simple, revolving primarily around the AJAX request and responses. There are two interactive components, the criteria selection and the comparisons. A final sortable table of results is generated <mark>(along with a map)</mark>.
### Lessons Learned:
I don’t really like Javascript, and I appreciate Python more now. Performing basic matrix manipulations was much more painful in Javascript (probably because I don’t really know what I’m doing). There were countless moments where I said to myself “I know this can’t be optimal way to write this, but it’s the only way I know.” For my next project I need to either choose a different backend language or really invest in learning proper Javascript.
### Next Steps:
I would like to add more criteria and more data. I’ll admit that the applicability of this project is highly personal and somewhat limited, so I would like to explore similar applications such as college choice, car buying, or real estate investment.


## Data Sources
Wikipedia: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population
Bureau of Economic Analysis: https://www.bea.gov/regional/downloadzip.cfm
Zillow: https://www.zillow.com/research/data/
Walkscore: https://www.walkscore.com/cities-and-neighborhoods/
National Oceanic and Atmospheric Adminstration: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#data

v1.0
Cities List -> wikipedia.org
Criteria
 - Demographics
   - Population -> wikipedia.org
   - Population Density -> wikipedia.org
 - Cost
   - Housing Prices -> zillow.com
   - Regional Price Parity -> Bureau of Economic Analysis
 - Climate
   - Longterm Avg Annual Low -> ncdc.noaa.gov 
   - Longterm Avg Annual High -> ncdc.noaa.gov
   - Longterm Avg Precipitation Total -> ncdc.noaa.gov
 - Mobility
   - Walkability -> walkscore.com
   - Bikability -> walkscore.com
   - Public Transit -> walkscore.com

v2.0
Cities List -> wikipedia.org
Geographic Filtering -> Click on map, sort by distanct from selected point
Criteria
 - Demographics
   - Population -> wikipedia.org
   - Population Density -> wikipedia.org
 - Cost
   - Housing Prices -> zillow.com
   - Regional Price Parity -> Bureau of Economic Analysis
   - Taxes -> State-specific?
 - Climate
   - Longterm Avg Annual Low -> ncdc.noaa.gov 
   - Longterm Avg Annual High -> ncdc.noaa.gov
   - Longterm Avg Precipitation Total -> ncdc.noaa.gov
 - Culture
   - Distance to mountains or beaches -> ???
   - Wikipedia Article Length? -> wikipedia.org
   - Racial Diversity -> city-data.com
 - Mobility
   - Walkability -> walkscore.com
   - Bikability -> walkscore.com
   - Public Transit -> walkscore.com
 - Economic
   - Unemployment Rate -> city-data.com
   - Crime Rate -> city-data.com
   - Interconnectedness (e.g. number of airports)
   - Specific Career Selection -> Select from drop-down menu


## License
Copyright (c) 2017 nobleator

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
