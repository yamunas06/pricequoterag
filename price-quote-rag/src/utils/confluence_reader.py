import requests
# Used to remove html tags from string
import re

# Function to read contents of a Confluence page using JWT authentication
def read_confluence_page():
    # Parent URL
    url = "https://confluence.global.tesco.org/rest/api/content/search?cql=parent=142385606"

    # Set the Authorization header with the JWT token
    headers = {
        "TokenAuthWhitelistOK": "True"
    }

    # Make the GET request to 'parent' page
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()['results']

        # Loop through each page
        for element in json_response:
            url = "https://confluence.global.tesco.org/rest/api/content/"+element['id']+"?expand=body.view"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
                title = json_response['title']
                body = json_response['body']['view']['value']
                title_and_body = "Title: " + title + "\nContent: " + body
                print(remove_html_tags(title_and_body))

            else:
                # Handle errors
                print(f"Failed to retrieve page: {response.status_code} - {response.text}")
                return None

    else:
        # Handle errors
        print(f"Failed to retrieve page: {response.status_code} - {response.text}")
        return None
    
def remove_html_tags(dirty_content):
    CLEANR = re.compile('<.*?>') 
    clean_content = re.sub(CLEANR, '', dirty_content)
    return clean_content

# Example usage
if __name__ == "__main__":
    page_content = read_confluence_page()
    if page_content:
        print(page_content)
