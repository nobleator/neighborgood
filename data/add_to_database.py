import aggregator
import time
# import psycopg2
from ahp.models import Pollen, Walkability, Unemployment, CrimeRate


"""
Script that imports and runs aggregator.py to gather data, then writes to a
database.
This modularization enables aggregator.py to function solely as a scraper
returning JSON (?) data.
Write to database using built-in Django models.
Includes delay to run web scraping every 15 seconds to prevent overloading
servers.
"""

agg = aggregator.Aggregator()
zip_codes = []
for zip_code in zip_codes:
    pollen_results = agg.pollen_api(zip_code)
    p = Pollen(zip_code=zip_code,
               pollen_score=pollen_results['pollen rating'],
               date_accessed=pollen_results['access date'])
    p.save()
    walkability_results = agg.walkability_api(zip_code)
    w = Walkability(zip_code=zip_code,
                    walk_score=walkability_results['walkability rating'],
                    date_accessed=walkability_results['access date'])
    w.save()
    unemployment_results = agg.unemployment_api(zip_code)
    u = Unemployment(zip_code=zip_code,
                     unemployment=unemployment_results['avg unemployment'],
                     date_accessed=unemployment_results['access date'])
    agg.get_crime_cross_id()
    crime_results = agg.crime_rate_api(zip_code)
    c = CrimeRate(zip_code=zip_code,
                  crime_rate=crime_results['crime_rate'],
                  date_accessed=crime_results['access date'])
    time.sleep(15)
