# NeighborGood

## What It Is
This is a tool to help you find and choose a neighborhood to live in.

## How to Use It
Go to: <URL>, follow the instructions there.

## Changelog (and Planned Features)
### v1.0
- [] Page structure setup
- [] Demo data
- [] SQLite database
- [] Preferences
- [] Results heatmap (Mapbox API)
### v2.0
- [] Real data
- [] Migrate SQLite to PostgreSQL
- [] Deploy to Heroku
- [] Data export

## Design
Written in Go? NodeJS? Data aggregation with Python.
Python generates a database with tables for each criteria.
User selects criteria, then does a pairwise comparison. This comparison data is passed back to the server, where the weights are calculated, then utility is calculated for each criteria, using the database from before. This utility is turned into a GeoJSON dataset, where the circle radii equate to the overall utility. It also finds the top 5 locations with the highest utility. The GeoJSON data and the top 5 locations (and their utility) are passed back to the client. The client adds the GeoJSON data to the Mapbox image and puts the top 5 locations and utility into a sortable results table. The results table has a button for 'More results>', which sends a request for the next 5 highest scoring locations.

## Data Sources
City populations: https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk
City lat/lon populations and lat/lon: https://simplemaps.com/data/us-cities

Climate
- Pollen: pollen.com
- Summer high: ncdc.noaa.gov
- Winter low: ncdc.noaa.gov
- Humidity: ncdc.noaa.gov
Economic
- Unemployment: bls.gov
- Crime rate: ucrdatatool.gov
- Consumer price index: bls.gov
- Average income: irs.gov
Social
- Walkability: walkscore.com
- Parkland: parkscore.tpl.org
- School ratings: nces.ed.gov
- Business quality: yelp.com

## License
Copyright (c) 2017 nobleator

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
