import requests


def pollen_api(zip_code):
    """
    Scrape www.pollen.com for index ratings for a zip code

    rtype -> Python dictionary
    """
    url_form = 'https://www.pollen.com/api/forecast/current/pollen/'
    pollen_rating = -1
    ref = 'https://www.pollen.com/forecast/current/pollen/' + zip_code
    headers = {'Host': 'www.pollen.com',
               'Accept': 'application/json, text/plain, */*',
               'Referer': ref}
    response = requests.get(url_form + zip_code, headers=headers)
    pollen_periods = response.json()[u'Location'][u'periods']
    for period in pollen_periods:
        if period[u'Type'] == u'Today':
            pollen_rating = period[u'Index']
    result = {'zip code': zip_code,
              'pollen rating': pollen_rating}
    return result
