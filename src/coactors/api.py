import requests
import os
#remove
# import app
class API:
  # @classmethod
    @staticmethod
    def retrieve(route, querystring = {}):
    # url = "https://api.themoviedb.org/3/movie/550?api_key="
        url = "https://api.themoviedb.org/3" + route
        
        apiKey = os.environ['THEMOVIEDB_APIKEY'] 
        querystring['api_key']= apiKey

        # headers = {
        #   'x-rapidapi-key': apiKey,
        #   'x-rapidapi-host': "imdb8.p.rapidapi.com"
        #   }
        # app.api_count += 1
        # response = requests.request("GET", url, headers=headers, params=querystring)
        response = requests.request("GET", url, params=querystring)

        # print(response.text)    
        return response.text