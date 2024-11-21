import json
import os

import requests
from langchain.tools import tool


class SearchTools():

  @tool("Search internet")
  def search_internet(query):
    """Searches the internet when query is provided. Sample input is SearchTools.search_internet("whatisthemeaningoflife")"""
    return SearchTools.search(query)

  def search(query):
    params = json.dumps({"data": query})
    response = requests.request("GET", "http://localhost:5000/search?data=", params=params)
    results = response.json()
    
    print(type(results))  # Should show <class 'list'> or similar iterable
    print(results)
    
    content_list = []
    for result in results:
        try:
            content_list.append('\n'.join([
                    
                    f"Link: {result}",
                    
                    "\n-----------------"
                ]))
        except KeyError:
            continue  # Use 'continue' to skip to the next iteration

    content = '\n'.join(content_list)
    return f"\nSearch result: {content}\n"
  