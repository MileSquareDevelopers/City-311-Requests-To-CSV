# City 311 Requests To CSV
## Introduction
Many cities across North America offer a 311 service to its citizens, so they can report issues to their local officals. Typically the issues extend to tree trimming, sidewalk repair, streetlamp repair, or road repair. [Accella](https://www.accela.com/) offers this service to many cities under their product [PublicStuff](https://www.publicstuff.com/).

Using PublicStuff's API this script exports all public tickets from a communities 311 App and saves them to a CSV file. Export examples can be found in the [Collections Folder](https://github.com/MileSquareDevelopers/City-311-Requests-To-CSV/tree/master/Collections).

Please note this script only grabs public tickets.

### Script Prerequisites
Built a tested on Python 3.6.
* argparse
* requests
* csv

### Usage
#### Command Format
```
python3 ./get_data.py -o <output_file> -c <client_id>
```
#### Command Example 1
Gets the 311 tickets for client id 104 (New York City) and saves the data into a csv named results.csv.
```
python3 ./get_data.py -o results.csv -c 104
```

#### Command Example 2
Gets the 311 tickets for client id 1416 (Lazy Lake, FL) and saves the data into a csv named output.csv.
```
python3 ./get_data.py -o output.csv -c 1416
```
### FAQ
1. How do I find a cities client id?
A list of known city ID's can be found here.
Please note that the filename contains the time the list was generated, so the data could be old. You may need to consult with your communities 311 Service App or administrator.

2. Does this script work with 311 services not operated by Accella's Public Stuff?
No, sorry.

### Advanced Details
#### get_data.py
Contains the main method. User arguments are parsed via argparse. `main()` is called after the arguments are verified
##### main()
Creates a Acella_Api_Handler class objext, then runs the method get_data_and_write_to_csv().

#### accella_api_handler.py
Contains the class Acella_Api_Handler. `__init__` expects a `client_id` and `output_file`.
#### get_data_and_write_to_csv()
The method of the class the requests the data from Accella's API, parses the JSON response, and saves it to the out_file.
#### normalize_data(dict_item)
A static method that takes the API's json response and copies the fields from FIELD_DATA_FOR_CSV into `dict_for_csv`, which is then returned.
#### get_data()
Calls the API, increments the page counter by 1, and returns the json response from the Accella API.
