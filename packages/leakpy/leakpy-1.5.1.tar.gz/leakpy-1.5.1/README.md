# 🚀 LeakPy

LeakPy is a third-party client designed to seamlessly interact with the leakix.net API using Python.

> ❗ **Note:** This is **not** the official LeakIX client. Always refer to the [Official LeakIX Python Client](https://github.com/LeakIX/LeakIXClient-Python) for the official client.

## 📥 Installation

To install LeakPy via PyPi:

```bash
pip install leakpy
```

## 🖥️ CLI Usage 

```bash
$ leakpy -h
```

Options:

```plaintext
-h, --help            Show this help message and exit
-s {service,leak}, --scope {service,leak}
                        Type of information
-p PAGES, --pages PAGES
                        Define the number of pages
-q QUERY, --query QUERY
                        Specify the query
-P PLUGIN, --plugin PLUGIN
                        Specify a particular plugin
-o OUTPUT, --output OUTPUT
                        Output the results to a file
-r, --reset-api       Reset the saved API key
-lp, --list-plugins   List all available plugins
-f FIELDS, --fields FIELDS
                        Fields to extract from the JSON, comma-separated. Example: 'protocol,ip,port'
-sep SEPARATOR, --separator SEPARATOR
                        Separator for the extracted fields. Default is ','.
```

## 📘 Library Documentation

### LeakixScraper

The `LeakixScraper` class provides a direct and simple interface to the leakix.net API.

**Initialization:**

```python
from leakpy.scraper import LeakixScraper

scraper = LeakixScraper(api_key="Your_API_Key")
```

**Methods:**

- **execute(scope, query, pages, fields, sep)**

    Conduct a search on leakix.net.

    Arguments:
    - `scope` (str): Type of information (e.g., "service" or "leak").
    - `query` (str): The query to be executed.
    - `pages` (int): Number of pages to fetch.
    - `fields` (str): Fields to extract from the JSON, comma-separated (e.g., "event_source, host, ip, port").
    - `sep` (str): Separator for the extracted fields (default is ',').

    Example:

    ```python
    results = scraper.execute(scope="leak", query='+country:"France"', pages=10, fields="event_source, host, ip, port", sep=", ")
    print(results)
    ```

## 🚫 Disclaimer

LeakPy is an unofficial tool and is not affiliated with leakix.net. The developers of LeakPy are not responsible for any misuse or potential damage from this tool. Use responsibly and ensure you have the necessary permissions when accessing data.
