import requests

def top_result(query):
    response = requests.get('https://itunes.apple.com/search?term={}&limit=1'.format(query))
    json_response = response.json()
    if json_response['results']:
        result = json_response['results'][0]
    else:
        return False

    if not 'artistName' in result.keys():
        return False

    if not 'artistViewUrl' in result.keys():
        return False

    return {"name": result['artistName'], "url": result['artistViewUrl']}

def results(query, limit):
    response = requests.get('https://itunes.apple.com/search?term={}&limit={}'.format(query, limit))
    json_response = response.json()
    results = json_response['results']

    return results
