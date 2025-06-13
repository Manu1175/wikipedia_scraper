import requests
import re
import json
from bs4 import BeautifulSoup as bs
import pprint

def first_paragraph(wikipedia_url, session):

    req = session.get(wikipedia_url, timeout=10)
    req.raise_for_status() #returns HTTPerror if not working
    soup = bs(req.text,"lxml")
    
    paragraph = soup.find_all("p")

    parameter = r'([\[]).*?([\]])|[ⓘ]'
    
    for el in paragraph:
        paragraph_element = el.get_text(strip=True)
        for el2 in paragraph_element:
            if el2 == 'ⓘ':
                first_paragraph = paragraph_element
                break
            else:
                first_paragraph = paragraph[2].get_text()
                break
    
    string = first_paragraph
    first_paragraph = re.sub(parameter, '', string)
    return first_paragraph

def get_leaders():
    url="https://country-leaders.onrender.com"
    endpoints = ['/status', '/countries', '/cookie', '/leaders']
    
    session = requests.Session()  # Main session for API
    wiki_session = requests.Session()  # Separate session for Wikipedia
    
    if session.get(url+endpoints[0]):
        cookie_req = session.get(url+endpoints[2])
        cookies = cookie_req.cookies
        countries_req=session.get(url+endpoints[1], cookies=cookies)
        countries = countries_req.json()
        leaders_per_country ={}
    
        for country in countries:
            try:
                leaders_req = session.get(url+endpoints[3], cookies=cookies, params={'country': country})
                leaders = leaders_req.json()
         
                # Open wikipedia_url and Add first paragraph in dictionary
                for leader in leaders:
                    leader["first_paragraph"] = first_paragraph(leader['wikipedia_url'], wiki_session)
    
                leaders_per_country[country] = leaders     
            except  Exception as e:
                cookie_req = session.get(url + endpoints[2])
                cookies = cookie_req.cookies
                continue 
    else:
            print('Not succesful connection')
    return leaders_per_country

def save(leaders_per_country):
    pprint.pprint(leaders_per_country)
    try:
        with open("leaders_per_country.json", "w", encoding="utf-8") as f:
            json.dump(leaders_per_country, f, indent=4, ensure_ascii=False)
        print("Data successfully saved to leaders_per_country.json")
    except TypeError as e:
        print(f"JSON dump failed: {e}")
    except Exception as e:
        print(f"Unexpected error while saving: {e}")
        
# Main execution
data = get_leaders()
print(get_leaders())
save(get_leaders())