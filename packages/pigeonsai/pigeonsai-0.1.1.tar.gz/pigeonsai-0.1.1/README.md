# PigeonsAI SDK

The PigeonsAI SDK is a Python package that provides an interface to interact with the PigeonsDB database. This SDK allows you to search, initialize, get database information, and add documents to the database.

## Installation

To install the PigeonsAI SDK, use pip:

```
pip install pigeonsai
```

## Usage

To use the PigeonsAI SDK, first import the PigeonsDB class:

```
from pigeonsai import PigeonsDB
```


### Initialize the connection

Before using the SDK, you need to initialize the connection to the database by providing your API key and database name:


```
api_key = "your_api_key"
db_name = "your_db_name"
PigeonsDB.init(api_key, db_name)
```

### Add documents

To add documents to the database, use the add method:

```
documents = ["document1", "document2", "document3"]
metadata_list = [{"metadata1": "value1"}, {"metadata2": "value2"}, {"metadata3": "value3"}]

PigeonsDB.add(documents, metadata_list)
```


### Search

To search the database, use the search method:

```
query_text = "your_search_query"
k = 10  # Number of results to return
metadata_filters = [{"metadata1": "value1"}]  # Optional metadata filters
keywords = ["keyword"]  # Optional keywords

PigeonsDB.search(query_text, k, metadata_filters, keywords)
```


## Contributing

If you'd like to contribute to the PigeonsAI SDK, please submit a pull request or open an issue on the GitHub repository.

## License

The PigeonsAI SDK is released under the [MIT License](https://opensource.org/licenses/MIT) 
