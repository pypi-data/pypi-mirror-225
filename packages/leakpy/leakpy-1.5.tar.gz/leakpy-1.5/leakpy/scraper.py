#!/usr/bin/python3

import sys
import json
import time
import requests
import argparse
from bs4 import BeautifulSoup
from rich.console import Console
from os.path import exists, expanduser


class LeakixScraper:

    def __init__(self, api_key=None, verbose=False):
        """
        Initialize the LeakixScraper instance.
        
        Args:
            api_key (str): The API key for Leakix. Defaults to None.
            verbose (bool): If True, print additional debug information. Defaults to False.
        """
        self.console = Console()
        self.api_key_file = expanduser('~') + "/.local/.api.txt"
        self.api_key = api_key if api_key else self.read_api_key()
        self.verbose = verbose

    def log(self, *args, **kwargs):
        """
        Print log messages if verbose mode is enabled.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.verbose:
            self.console.print(*args, **kwargs)

    def execute(self, scope="leak", query="", pages=2, plugin=None):
        """
        Execute the scraper.
        
        Args:
            scope (str): The scope of the search. Defaults to "leak".
            query (str): The query parameter. Defaults to "".
            pages (int): Number of pages to scrape. Defaults to 2.
            plugin (str): The plugin name. Defaults to None.

        Returns:
            list: The scraped results.
        """
        
        plugins = self.get_plugins()

        if plugin and plugin not in plugins:
            raise ValueError(f"Invalid plugin. Valid plugins: {plugins}")

        results = self.query(scope, pages, query, plugin)
        return results
    
    def get_plugins(self):
        """
        Fetch the list of available plugins from Leakix.

        Returns:
            set: A set of tuples where each tuple contains a plugin name and its access level.
        """
        plugins_url = 'https://leakix.net/plugins'
        response = requests.get(plugins_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        row_elements = soup.find_all('div', {'class': 'row'})

        plugins = set()

        for row in row_elements:
            plugin_name_element = row.find('div', {'class': 'col-sm-3'})
            
            access_level_elements = row.find_all('div', {'class': 'col-sm-3'})
            if len(access_level_elements) > 1:
                access_level_element = access_level_elements[1]
            else:
                access_level_element = None

            if plugin_name_element and access_level_element:
                plugin_name = plugin_name_element.find('a').text.strip()
                access_level = access_level_element.find('em').text.strip() if access_level_element.find('em') else "Unknown"
                plugins.add((plugin_name, access_level))

        return plugins


    def save_api_key(self, api_key):
        """
        Save the provided API key to a file.
        
        Args:
            api_key (str): The API key to be saved.
        """
        with open(self.api_key_file, "w") as f:
            f.write(api_key)

    def read_api_key(self):
        """
        Read the API key from the file.
        
        Returns:
            str: The read API key or None if the file doesn't exist.
        """
        if not exists(self.api_key_file):
            return None

        with open(self.api_key_file, "r") as f:
            return f.read().strip()

    def query(self, scope, pages=2, query_param="", plugin=None):
        """
        Query the Leakix website and get results.
        
        Args:
            scope (str): The scope of the search.
            pages (int): Number of pages to scrape. Defaults to 2.
            query_param (str): The query parameter. Defaults to "".
            plugin (str): The plugin name. Defaults to None.

        Returns:
            list: List of found targets.
        """
        if plugin:
            query_param += f" +plugin:{plugin}"

        results = []

        for page in range(pages):
            self.log(f"[bold green]\n[-] Query {page + 1} : \n")
            response = requests.get(
                "https://leakix.net/search",
                params={"page": str(page), "q": query_param, "scope": scope},
                headers={"api-key": self.api_key, "Accept": "application/json"},
            )

            if response.text == "null":
                self.log("[bold yellow][!] No more results available (Please check your query or scope)")
                break
            elif response.text == '{"Error":"Page limit"}':
                self.log(f"[bold red][X] Error : Page Limit for free users and non users ({page})")
                break

            try:
                data = json.loads(response.text)
                for json_data in data[1:]:
                    protocol = f"{json_data['protocol']}://"
                    protocol = protocol if protocol in {"http://", "https://"} else ""
                    target = f"{protocol}{json_data['ip']}:{json_data['port']}"
                    if target not in results:
                        self.log(f"[bold blue][+] {target}")  
                        results.append(target)
            except json.JSONDecodeError:
                self.log("[bold yellow][!] No more results available (Please check your query or scope)")
                break

            time.sleep(1.2)
        return results



    def run(self, scope, pages=2, query_param="", plugin=None, output=None):
        """
        Main function to start the scraping process.
        
        Args:
            scope (str): The scope of the search.
            pages (int): Number of pages to scrape. Defaults to 2.
            query_param (str): The query parameter. Defaults to "".
            plugin (str): The plugin name. Defaults to None.
            output (str): The filename to save the scraped results. Defaults to None.
        """
        
        plugins = self.get_plugins()
        plugin_names = {plugin_name for plugin_name, _ in plugins}

        if plugin and plugin not in plugin_names:
            self.log("\n[bold red][X] Plugin is not valid")
            self.log(f"[bold yellow][!] Plugins available : {len(plugins)}\n")
            for plugin_name, access in plugins:
                self.log(f"[bold cyan][+] {plugin_name} - {access}")
            sys.exit(1)

        if not self.api_key or len(self.api_key) != 48:
            self.api_key = input("Please Specify your API Key (leave blank if you don't have) : ")
            self.save_api_key(self.api_key)

        if not self.api_key:
            self.log(f"\n[bold yellow][!] Querying without API Key...\n (remove or edit {self.api_key_file} to add API Key if you have)")
        else:
            self.log("\n[bold green][+] Using API Key for queries...\n")

        results = self.query(scope, pages, query_param, plugin)

        if output:
            with open(output, "w") as f:
                for result in results:
                    f.write(f"{result}\n")
            self.log(f"\n[bold green][+] File written successfully to {output} with {len(results)} lines\n")

def main():
    console = Console()
    
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-s", "--scope", choices=["service", "leak"], default="leak", help="Type Of Informations", type=str)
        parser.add_argument("-p", "--pages", help="Number Of Pages", default=2, type=int)
        parser.add_argument("-q", "--query", help="Specify The Query", default="", type=str)
        parser.add_argument("-P", "--plugin", help="Specify The Plugin", type=str)
        parser.add_argument("-o", "--output", help="Output File", type=str)
        parser.add_argument("-lp", "--list-plugins", action="store_true", help="List Available Plugins")
        parser.add_argument("--reset-api", action="store_true", help="Reset the API key")
        
        args = parser.parse_args()

        scraper = LeakixScraper(verbose=True)
        
        if args.reset_api:
            new_api_key = input("[!] Please enter your new API Key: ")
            scraper.save_api_key(new_api_key)
            console.print("[bold green][+] API key updated successfully![/bold green]")
            sys.exit(0)
    
        if args.list_plugins:
            plugins = scraper.get_plugins()
            console.print(f"[bold yellow][!] Plugins available : {len(plugins)}\n")
            for plugin, access in plugins:
                console.print(f"[bold cyan][+] {plugin} - {access}")
            sys.exit(0)    
                
        scraper.run(args.scope, args.pages, args.query, args.plugin, args.output)
        
    except Exception as e:
        console.print(f"\n[bold red][X] An error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
