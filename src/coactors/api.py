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
        
        api_key = API.get_secret("THEMOVIEDB_APIKEY")
        
        querystring['api_key']= api_key

        response = requests.request("GET", url, params=querystring)
    
        return response.text

    @staticmethod
    def get_secret_helper(project_id, secret_id, version_id):
        """
        Access the payload for the given secret version if one exists. The version
        can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Import the Secret Manager client library.
        from google.cloud import secretmanager

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        return response.payload.data.decode("UTF-8")

    @staticmethod
    def get_secret(key):
        try:
            return os.environ['THEMOVIEDB_APIKEY']
        except KeyError:
            print("getting the secret - print")

            api_key = API.access_secret_version("508429297891", key, 1)
            os.environ['THEMOVIEDB_APIKEY'] = api_key
            return api_key