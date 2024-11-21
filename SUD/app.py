import subprocess
from flask import Flask, request, jsonify
import json
import sys
import urllib.parse

app = Flask(__name__)

def run_js_playwright_script(search_query):
    # Replace 'script.js' with the path to your JavaScript file
    js_script_path = 'script.js'
    
    # Run the Node.js script using subprocess.run
    # Pass the search query as a command-line argument to your JavaScript script
    result = subprocess.run(['node', js_script_path, search_query], capture_output=True, text=True)

    # Check if there was an error
    if result.returncode != 0:
        # Returning error details and status code
        return {'error': result.stderr.decode()}, 500
    else:
        try:
            # Parse and return the JSON output from your Playwright script
            urls = json.loads(result.stdout)
            return urls, 200  # Returning result and HTTP status code
        except json.JSONDecodeError:
            return {'error': 'Failed to parse JSON output'}, 500
        
@app.route('/search')
def search():
    # Get the full query string
    full_query_string = request.query_string.decode()
    
    # Attempt to clean up the query string
    # Remove 'data=' and any other unwanted characters before the JSON object
    cleaned_query = full_query_string.replace('data=&', '')

    # URL-decode the cleaned query string
    decoded_query = urllib.parse.unquote(cleaned_query)

    # Now, attempt to parse the JSON from the decoded query
    try:
        query_data = json.loads(decoded_query)
        search_query = query_data.get('data')
        if not search_query:
            return jsonify({'error': 'Missing "data" in query parameter'}), 400
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400

    urls, status_code = run_js_playwright_script(search_query)
    return jsonify(urls), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)