import requests


def fetch_data(api_url):
    page = 1
    citations = []

    while True:
        try:
            response = requests.get(api_url, params={'page': page})
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            break
        except ValueError as e:
            print(f"JSON decoding failed: {e}")
            break

        print("Page", page, "data:", data)  # Debugging output

        if 'data' not in data or not data['data']:
            break

        for item in data['data']:
            if isinstance(item, dict):
                citations.extend(get_citations(item))

        if 'next_page_url' not in data:
            break

        page += 1

    return citations


def get_citations(item):
    citations = []
    if 'source' in item and isinstance(item['source'], list):
        for source in item['source']:
            if isinstance(source, dict):
                citations.append({'id': source.get('id'), 'link': source.get('link', '')})
    return citations


def main():
    api_url = 'https://devapi.beyondchats.com/api/get_message_with_sources'
    citations = fetch_data(api_url)
    print(citations)


if __name__ == "__main__":
    main()
