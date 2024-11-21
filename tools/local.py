import json
import logging
from langchain.tools import tool
import subprocess
import os    # Path: \home\supai\CrewAI\tools\local.py

logging.basicConfig(level=logging.INFO, filename='tool_usage1.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

path_parts = ["/home", "supai", "CrewAI", "search.js"]

class LocalSearchTool:
    @staticmethod
    @tool("Search internet")
    def local_search(query):
        """
        Useful to search the internet about a given topic and return urls.
        Here, `query` is the tool input, which is what the user wants to search for.
        """
        node_path = "node"
        js_file_path = os.path.join(*path_parts)
        

        try:
            # Pass the argument as a separate item in the list
            results = subprocess.run([node_path, js_file_path, query], check=True, capture_output=True, text=True)
           
            output = results.stdout
            print(output)
            return '\n'.join(output)

            # Assuming the JS script outputs the results
            print(output)
            return output
    
        except subprocess.CalledProcessError as e:
            print(f"Error executing search.js: {e}")
            return "An error occurred while executing the search"
        


tool = LocalSearchTool()
query = "Best travel websites"
result = tool.local_search(query)