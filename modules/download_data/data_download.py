""" Downloading data from OMDB API and parsing it into proper dict """

import concurrent.futures
import os
import requests


class DataDownloader:
    """ Data downloading class """

    @property
    def api_key(self):
        """
        Read API key from env variable
        :return api_key: api key environmental variable
        :raises ValueError: env variable OMDB_API_KEY is not set
        """

        api_key = os.environ.get('OMDB_API_KEY')

        if api_key is None:
            raise ValueError('OMDB API KEY not set as env variable!')

        return api_key

    def download_data(self, list_of_titles):
        """
        Downloading and parsing data
        :param list_of_titles: list of titles to download
        :return: dict containing downloaded and parsed data
        """

        # Download the data using API
        with concurrent.futures.ThreadPoolExecutor() as executor:
            downloaded_data = executor.map(self.download_title, list_of_titles)

        # Parse downloaded data
        with concurrent.futures.ProcessPoolExecutor() as executor:
            parsed_data = executor.map(self.parse_json_response, downloaded_data)

        # Filter out None results from parsed data
        filtered_data = filter(lambda x: x is not None, parsed_data)

        return filtered_data

    def download_title(self, title):
        """
        Downloading a single title
        :param title: title of movie to download its data
        :return: response from GET request
        """

        payload = {'t': title, 'r': 'json'}  # Payload params for url request
        response = requests.get(f'http://www.omdbapi.com/?apikey={self.api_key}',
                                params=payload).json()

        return response

    def parse_json_response(self, response):
        """
        Parsing downloaded json response
        :param response: json response from GET request to OMDB API
        :return result: result dict with parsed values, None if incorrect json response
        :raises KeyError: incorrect json response which can;t be parsed
        """

        result = None

        try:
            year = int(response['Year'])  # json response in in str
            imdb_rating = float(response['imdbRating'])  # json response is in str
            imdb_votes = self.leave_digits(response['imdbVotes'])
            box_office = self.leave_digits(response['BoxOffice'])

            result = {'Title': response['Title'], 'Year': year,
                      'Runtime': response['Runtime'], 'Genre': response['Genre'],
                      'Director': response['Director'], 'Writer': response['Writer'],
                      'Cast': response['Actors'], 'Language': response['Language'],
                      'Country': response['Country'], 'Awards': response['Awards'],
                      'imdbRating': imdb_rating, 'imdbVotes': imdb_votes,
                      'BoxOffice': box_office}
        except KeyError:
            print(f'Cannnot parse response: {response}')

        return result

    @staticmethod
    def leave_digits(number_to_convert):
        """
        Leave digits of number string containing chars like ',' or '$'
        :param number_to_convert: number string with special characters
        :return: number converted to integer or None if no digit found
        """
        try:
            converted = int(''.join(i for i in number_to_convert if i.isdigit()))
            return converted
        except ValueError:
            return None
