import urllib.request
import urllib.parse
import json
import argparse
from pathlib import Path

#
# API
#

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
    selected_mod = search_json['hits'][x]

    print(f'Selected mod: {selected_mod['title']}')
    return selected_mod['project_id']

#
# FILE
#

def init_instance_file(args):
    file = Path('modlist.json')

    init_data = {
        'version': args.version,
        'modloader': args.modloader,
        'mods': []
        }

    if file.exists():
        if args.overwrite:
            print('Overwriting the instance file')

            with file.open(mode='w', encoding='utf-8') as f:
                json.dump(init_data, f, indent=4, ensure_ascii=False)

        else:
            print('Instance file already exists. Use -o flag to overwrite')
    else:
        print('Writing the instance file')

        with file.open(mode='w', encoding='utf-8') as f:
            json.dump(init_data, f, indent=4, ensure_ascii=False)

#
# ARGUMENT PARSING
#

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand', required=True)

sub_init = subparsers.add_parser('init', help='Initialize an instance')
sub_init.add_argument('-v', '--version', help='Minecraft version of the instance e.g. 1.21.1', required=True)
sub_init.add_argument('-m', '--modloader', help='Modloader of the instance e.g. fabric', required=True)
sub_init.add_argument('-o', '--overwrite', help='Overwrite the instance file if exits', default=False, action='store_true')
sub_init.set_defaults(func=init_instance_file)

args = parser.parse_args()
args.func(args)
