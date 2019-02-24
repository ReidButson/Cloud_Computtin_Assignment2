import requests
import feedparser

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

    return {"name": result['artistName'], "url": result['artistViewUrl'], "image": result['artworkUrl100']}

def results(query, limit):
    response = requests.get('https://itunes.apple.com/search?term={}&limit={}'.format(query, limit))
    json_response = response.json()
    results = json_response['results']

    return results

def podcasts(query):
    response = requests.get('https://itunes.apple.com/search?term={}&entity=podcast&limit=10'.format(query))
    json_response = response.json()
    podcast = json_response['results'][0]

    feed_URL = podcast['feedUrl']
    feed = feedparser.parse(feed_URL)

    episodes = []
    limit = len(feed.entries)
    if limit > 50:
        limit = 50

    for i in range(limit):
        entry = feed.entries[i]
        pod_url = ''
        if 'media_content' in entry.keys():
            pod_url = entry.media_content[0]['url']

        elif 'links' in entry.keys():
            audio_link = [link['href'] for link in entry.links if 'audio/' in link['type'] or 'video/mp4' in link['type']]
            pod_url = audio_link[0]
        episodes.append({'name': entry['title'], 'url': pod_url})

    return episodes
