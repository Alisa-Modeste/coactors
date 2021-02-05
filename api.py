import requests
import os
#remove
import app
class API:
  # @classmethod
  @staticmethod
  def retrieve(route, querystring):
  # url = "https://imdb8.p.rapidapi.com/title/get-top-cast"
    url = "https://imdb8.p.rapidapi.com/" + route
    
    apiKey = os.environ['IMDB_APIKEY'] 
    # querystring = {"tconst":"tt0944947"}

    headers = {
      'x-rapidapi-key': apiKey,
      'x-rapidapi-host': "imdb8.p.rapidapi.com"
      }
    app.api_count += 1
    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)    
    return response.text