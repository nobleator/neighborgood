"""BLS Data
https://www.bls.gov/help/hlpforma.htm#WP


Employment & Unemployment
Nonfarm Payroll Statistics from the Current Employment Statistics (National)
    National Employment, Hours, and Earnings
    National Employment, Hours, and Earnings (SIC basis)
Nonfarm Payroll Statistics from the Current Employment Statistics (State & Area)
    State and Area Employment, Hours, and Earnings
    State and Area Employment, Hours, and Earnings (SIC basis)
Quarterly Census of Employment and Wages
    State and County Employment and Wages from Quarterly Census of Employment and Wages
    State and County Employment and Wages from Quarterly Census of Employment and Wages, 1997-2000 (SIC basis)
Occupational Employment Statistics
Business Employment Dynamics
Local Area Unemployment Statistics
    Local Area Unemployment Statistics
    Geographic Profile
Mass Layoff Statistics
Job Openings and Labor Turnover Survey
    Job Openings and Labor Turnover Survey
    Job Openings and Labor Turnover Survey (SIC basis)
Green Goods and Services

Spending & Time Use
American Time Use Survey
Consumer Expenditure Survey

Inflation & Prices
Consumer Price Indexes
    Average Price Data
    Consumer Price Index-All Urban Consumers (Current Series)
    Consumer Price Index-Urban Wage Earners and Clerical Workers (Current Series)
    Consumer Price Index-All Urban Consumers (Old Series)
    Consumer Price Index-Urban Wage Earners and Clerical Workers (Old Series)
    Department Store Inventory Price Index
    Chained CPI-All Urban Consumers
Producer Price Indexes
    Producer Price Index Industry Data - Current Series
    Producer Price Index Industry Data - Discontinued Series (NAICS basis)
    Producer Price Index Industry Data - Discontinued Series (SIC basis)
    Producer Price Index Commodity Data - Current Series
    Producer Price Index Commodity Data - Discontinued Series
Pay & Benefits
Collective Bargaining Agreements
    Work Stoppage Data
Employee Benefits Survey
Employment Cost Index (SIC)
Employer Cost for Employee Compensation (SIC)
National Compensation Survey
Modeled Wage Estimates

Productivity
Major Sector Productivity and Costs
Major Sector Multifactor Productivity
Industry Productivity

Workplace Injuries
Injuries, Illnesses, & Fatalities
    Occupational injuries and illnesses: industry data (2014 forward)
    Census of Fatal Occupational Injuries (2011 forward)
    Census of Fatal Occupational Injuries (2003 - 2010)
    Census of Fatal Occupational Injuries (1992 - 2002)
    Nonfatal cases involving days away from work: selected characteristics (2011 forward)
    Nonfatal cases involving days away from work: selected characteristics (2003 - 2010)
    Nonfatal cases involving days away from work: selected characteristics (2002)
    Nonfatal cases involving days away from work: selected characteristics (1992 - 2001)
    Occupational injuries and illnesses: industry data (pre-1989)
    Occupational injuries and illnesses: industry data (1989 - 2001)
    Occupational injuries and illnesses: industry data (2002)
    Occupational injuries and illnesses: industry data (2003 - 2013)

Occupational Requirements
    Occupational Requirements Survey

International
    Import and Export Price Indexes
"""

# Create SQLite database with tables for each of the BLS series
import sqlite3
import requests


def set_fips():
    """Initialize table in bls.db for FIPS codes
    """
    conn = sqlite3.connect('bls.db')
    curs = conn.cursor()
    comm = """
           CREATE TABLE IF NOT EXISTS fips
           (state TEXT, statefp TEXT,
           countyfp TEXT, countyname TEXT, classfp TEXT)
           """
    curs.execute(comm)
    conn.commit()
    comm = 'INSERT INTO fips VALUES (?, ?, ?, ?, ?)'
    url = 'https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt'
    resp = requests.get(url)
    for line in resp.text.split('\n'):
        if len(line) < 5:
            continue
        line_list = line.split(',')
        # Strip carriage return character
        line_list[-1] = line_list[-1][:-1]
        curs.execute(comm, tuple(line_list))

    conn.commit()
    conn.close()


def get_fips(query):
    """
    Returns list of FIPS codes (strings) that most closely match input query
    """
    pass


def set_bls_data():
    pass


if __name__ == '__main__':
    # set_fips()
    set_bls_data()
