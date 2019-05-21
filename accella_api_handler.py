import requests
import csv

class Acella_Api_Handler:
    """
    This class pretty much does it all. It handles calls to Accella's Public Stuff API Interface,
    and exports the data to a CSV.
    """
    class APIError(Exception): pass
    PUBLICSTUFF_API_URL = 'https://vc0.publicstuff.com/api/2.0/requests_list?api_key={API_KEY}&client_id={CLIENT_ID}&device=iframe&limit={LIMIT}'
    LIMIT = 45 # Number of requests to ask from the API. Max appears to be 46.
    REQUESTS_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
    # The fields we want saved in the CSV.
    FIELD_DATA_FOR_CSV = {'primary_attachment url': 'Attachment URL', 'id': 'ID', 'title': 'Title',
                          'description': 'Description', 'status': 'Status', 'address': 'Address', 'location': 'Location',
                          'zipcode': 'Zip Code','date_created': 'Date Created', 'count_comments': 'Num Of Comments',
                          'count_followers': 'Num Of Followers', 'count_supporters': 'Num Of Supporters',
                          'lat': 'Latitude', 'lon': 'Longitude', 'rank': 'Rank', 'user': 'User'}

    def __init__(self, api_key, client_id, out_file):
        """
        This is the main method. This method makes a call to Accella's API interface requesting all public
        :param api_key: The API key used to connect the Public Stuff API. This should be 20 characters long.
        :param client_id: The client id used to connect to the Public Stuff API.
        :param out_file: The destination file for the CSV.
        """

        # Check if the API key is 20 characters.
        if len(api_key) != 20:
            while True:
                print ("API key seems incorrect. It should be 20 characters. Continue?")
                choice = input().lower()
                if choice == 'yes' or choice == 'y':
                    break
                if choice == 'no' or choice == 'n':
                    raise ValueError('API Key should be 20 characters in length.')
                print('Invalid response. Please answer with y/n.')
        self.out_file = out_file  # The location where the csv will be saved.
        self.current_page = 0  # Tracks the current page
        self.last_page = False # Tracks if the last page was returned.
        self.api_url = self.PUBLICSTUFF_API_URL.replace('{API_KEY}', api_key)\
            .replace('{CLIENT_ID}', client_id)\
            .replace('{LIMIT}', str(self.LIMIT))

    def get_data(self):
        """
        Uses requests to call self.api_url and returns the data as JSON.
        :return: JSON data if valid. False if data is not valid or there is none left.
        """
        if self.last_page:
            """
            We check if the self.last_Page variable is set to True. This gets set when the response is 
            less than the Acella_Api_Handler.LIMIT int.
            """
            return False

        api_url = '%s%i' % (self.api_url, self.current_page)  # Build the api_url. Essentially api_url + current_page

        # The api doesn't work with page 0. Check if we're at page 0. If we are NOT, then add the page.
        if self.current_page >= 1:
            api_url = '%s%s%i' % (api_url, '&page=', self.current_page)

        response = requests.get(url=api_url, headers=self.REQUESTS_HEADERS).json()  # Get page and return data as JSON
        response_status = response['response']['status']['type'].lower() # Get the status from the API.
        if response_status == 'error': # If API returns a status type of error then raise an error.
            raise Acella_Api_Handler.APIError('API responded with error {}'
                                              .format(response['response']['status']['code_message']))
            return False
        elif len(response['response']['requests']) < self.LIMIT:
            # The API gave us less than the limit. We know we're at the last page.
            self.last_page = True
        elif len(response['response']['requests']) <= 0: # The API gave us no more data. We must be done.
            self.last_page = True
            return False
        self.current_page += 1  # Increment the current page by 1.
        return response['response']['requests']

    @staticmethod
    def normalize_data(dict_item):
        """
        Gets a dict item from the PublicStuff API and normalizes it.
        :return: A dict of items to write to CSV.
        """
        dict_for_csv = {}
        # Loop through FIELD_DATA_FOR_CSV to pull the fields we want.
        for key, value in Acella_Api_Handler.FIELD_DATA_FOR_CSV.items():
            # We save the prettified field name by using the value of Acella_Api_Handler.FIELD_DATA_FOR_CSV.
            dict_for_csv[value] = dict_item['request'].get(key, 'NA')

        # TODO figure out how to access nested loops so you don't hardcode this.
        if dict_item['request'].get('primary_attachment', False):
            dict_for_csv['Attachment URL'] = dict_item['request']['primary_attachment'].get('url', 'NA')
        return dict_for_csv




    def get_data_and_write_to_csv(self):
        """
        Gets the data from the PUBLICSTUFF_API_URL and writes it to the out_file. Returns true if successful.
        :returns True if successful.
        """
        request_data = True # The variable that will store the JSON response
        # Open the CSV for writing.
        with open(self.out_file, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.FIELD_DATA_FOR_CSV.values())  # Get the headers
            csv_writer.writeheader()  # Write the header

            # While we have NOT received False from get_data() we keep running.
            while request_data:
                print('Getting page ', self.current_page)
                request_data = self.get_data()  # Get the data via the api save response to request_data.
                for data in request_data: # Loop through each data field.
                    dict_for_csv = self.normalize_data(data)
                    csv_writer.writerow(dict_for_csv)  # Write the prettified data to the csv file.
