import requests
from api_key import *
from crawler import *

class FetchFromAPI:

    def __init__(self):
        self.url = "https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url"
        self.headers = {
            "x-rapidapi-key": "07b09109eamshe6ffaa5916c6cc3p181168jsnfb9b4c61ce99",
            "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
        }

    def fetch(self, profileLink : str) -> dict:

        querystring = {"url": profileLink}

        response = requests.get(self.url, headers = self.headers, params = querystring)

        results = {'username': None,
                     'firstName': None,
                     'lastName': None, 
                     'country': None, 
                     'city': None, 
                     'company': None,
                     'position': None,
                     'profileLink': profileLink,
                     'email-1': None,
                     'email-2': None,
                     'email-3': None
                     }

        results['username'] = response.json().get('username',None)
        results['firstName'] = response.json().get('firstName',None)
        results['lastName'] = response.json().get('lastName',None)

        check_geo = response.json().get('geo',None)

        if check_geo:
            results['country'] = response.json()['geo']['country']
            results['city'] = response.json()['geo']['city']

        check_position = response.json().get('position')

        if  check_position:
            results['company'] = response.json()['position'][0]['companyName']
            results['position'] = response.json()['position'][0]['title']

        return results
    

# if __name__ == "__main__":

#     crawler = Crawler("devverma269@gmail.com","!R0nald0!")

#     fetchapi = FetchFromAPI()

#     links = crawler.crawl("deloitte",'hr')
#     crawler.close()
 
#     data = []
#     data.append(fetchapi.fetch(links[0]))

#     print(data)





