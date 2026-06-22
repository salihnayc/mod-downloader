import urllib.request
import urllib.parse
import json

def api_request(path, **query_params):
    base_url = f'https://api.modrinth.com/v2/{path}'

    query_string = urllib.parse.urlencode(query_params)

    url = f'{base_url}?{query_string}'

    headers = {'User-Agent': 'salihnayc/mod-downloader'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        data_raw = response.read().decode('utf-8')
        data_json = json.loads(data_raw)

    return data_json

def make_selection(array, question, *values):
    n = 1
    for i in array:
        print(n, end='')
        for j in values:
            print(f' - {i[j]}', end='')
        print()
        n += 1
        
    x = int(input(question))
    return x - 1

def search_mods(mod_name, modloader, minecraft_version, search_limit):
    facet = f'[["project_type=mod"],["categories:{modloader}"],["versions:{minecraft_version}"]]'
    search_json = api_request('search', query=mod_name, facets=facet, limit=search_limit)

    x = make_selection(search_json['hits'], 'Select a mod e.g. 2: ', 'title', 'description')
    print(f'Selected mod: {search_json['hits'][x]['title']}')

search_mods('sodium', 'fabric', '26.1.2', 5)