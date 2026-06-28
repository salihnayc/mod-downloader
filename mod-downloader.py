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

def search_mod(mod_name, modloader, minecraft_version):
    facet = f'[["project_type=mod"],["categories:{modloader}"],["versions:{minecraft_version}"]]'
    search_json = api_request('search', query=mod_name, facets=facet)

    x = make_selection(search_json['hits'], 'Select a mod e.g. 2: ', 'title', 'description')
    selected_mod_name = search_json['hits'][x]['title']
    selected_mod_id = search_json['hits'][x]['project_id']

    selected_mod_data = {'mod_name': selected_mod_name, 'mod_id': selected_mod_id}
    return selected_mod_data

def search_version(mod_id, modloader, minecraft_version):
    version_json = api_request(f'project/{mod_id}/version', loaders=f'["{modloader}"]', game_versions=f'["{minecraft_version}"]', include_changelog='false')

    x=make_selection(version_json, 'Select a version. 2: ', 'name')
    selected_version_name = version_json[x]['name']
    selected_version_id = version_json[x]['id']

    selected_version_data = {'version_name': selected_version_name, 'version_id': selected_version_id}
    return selected_version_data

#
# FILE
#

def read_json_from_file(file):
    with file.open(mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json_to_file(file, data):
    with file.open(mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

#
# ARGUMENT FUNCTIONS
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
            write_json_to_file(file, init_data)
        else:
            print('Instance file already exists. Use -o flag to overwrite')
    else:
        print('Writing the instance file')
        write_json_to_file(file, init_data)

def add_mods(args):
    file = Path('modlist.json')

    if file.exists():
        data = read_json_from_file(file)
        mod_data = search_mod(args.name, data['modloader'], data['version'])
        version_data = search_version(mod_data['mod_id'], data['modloader'], data['version'])

        mod_dict = mod_data | version_data
        
        data['mods'].append(mod_dict)

        write_json_to_file(file, data)

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

sub_add = subparsers.add_parser('add', help='Add a mod to the instance file')
sub_add.add_argument('name', help='Name of the mod')
sub_add.add_argument('-l', '--latest', help='Autoselect the latest release of the mod', default=False, action='store_true')
sub_add.set_defaults(func=add_mods)

args = parser.parse_args()
args.func(args)
