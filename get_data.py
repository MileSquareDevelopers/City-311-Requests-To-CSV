import argparse
from accella_api_handler import Acella_Api_Handler

def main(api_key, client_id, out_file):
    """The main method which controls the Acella_Api_Handler class"""

    api = Acella_Api_Handler(api_key, client_id, out_file)
    api.get_data_and_write_to_csv()

if __name__ == '__main__':
    """
    Parse arguments, check they are valid, and run main.
    """
    parser = argparse.ArgumentParser(description='Recursively grabs all public requests from Accella\'s PublicStuff.')
    parser.add_argument('-a', '--api', help='The API key to access the Accella Publicstuff data.',
                        type=str, dest='api_key', required=True)
    parser.add_argument('-c', '--clientID', help='The community\'s client ID.',
                        type=int, dest='client_id', required=True)
    parser.add_argument('-o', '--output', help='The destination file containing the public requests from PublicStuff.',
                        type=str, dest='out_file', required=True)
    args = parser.parse_args()
    main(args.api_key, str(args.client_id), args.out_file)