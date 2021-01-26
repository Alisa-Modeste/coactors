import requests

def(route, querystring):
# url = "https://imdb8.p.rapidapi.com/title/get-top-cast"
  url = "https://imdb8.p.rapidapi.com/" + route
  # querystring = {"tconst":"tt0944947"}

  headers = {
    'x-rapidapi-key': apiKey,
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(response.text)    