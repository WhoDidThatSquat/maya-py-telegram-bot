from bs4 import BeautifulSoup
import urllib
import unicodedata
import json
import pprint

def get_covid_city_stats(city):
    url = "https://datelazi.ro/embed/large-cities-incidents-table"
    url_contents = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(url_contents, "html.parser")
    tagged_content = soup.find("script", {"id": "__NEXT_DATA__"})
    for data in tagged_content(['script']):
        data.decompose()

    city_normalized = unicodedata.normalize('NFKD',city).encode('ascii','ignore')
    city_str = city_normalized.decode("utf-8")

    content_json_unicode = ''.join(tagged_content.stripped_strings)
    content_json_normalized = unicodedata.normalize('NFKD',content_json_unicode).encode('ascii','ignore')
    content_json_str = content_json_normalized.decode("utf-8")
    loaded = json.loads(content_json_str)
    last_updated = ''.join(loaded["props"]["pageProps"]["data"]["currentDayStats"]["parsedOnString"])
    #print(last_updated)
    #county_incidence = loaded["props"]["pageProps"]["data"]["currentDayStats"]["incidence"]
    large_cities_incidence = loaded["props"]["pageProps"]["data"]["currentDayStats"]["large_cities_incidence"]
    small_cities_incidence = loaded["props"]["pageProps"]["data"]["currentDayStats"]["small_cities_incidence"]
    cities = small_cities_incidence + large_cities_incidence
    city_list = []


    for item in cities:
        city_details = {"Nr.crt.": None, "Judet": None, "Localitate": None, 'Populatie': None, "Cazuri": None, "Incidenta": None}
        city_str = city_str.upper()

        if city_str in item['Localitate']:
            #city_details['Nr.crt.'] = item['Nr.crt.']
            city_details['Judet'] = item['Judet']
            city_details['Localitate'] = item['Localitate']
            city_details['Populatie'] = item['Populatie']
            city_details['Cazuri'] = item['Cazuri']
            city_details['Incidenta'] = item['Incidenta']
            city_details['last_updated'] = last_updated
            city_list.append(city_details)
    return city_list




