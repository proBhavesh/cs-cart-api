import requests


def get_all_pages(base_url, api_key):
    """
    This function retrieves all pages from the CS-Cart API.
    """

    # Define the URL for the Pages entity
    url = f"{base_url}/api/2.0/pages"

    # Define the headers for the request
    headers = {
        "Authorization": f"Basic {api_key}",
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Print the pages
        print(json_response)
    else:
        print("Request failed with status code", response)


# Example usage:
get_all_pages("https://shop.migoiq.app", "684af83aebfdf868a4dacb727e6deecd")
