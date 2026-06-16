import requests
import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-n','--name',help='Name of the mod', required=True)
arg_parser.add_argument('-m','--modloader',help='Modloader of the mod', required=True)
arg_parser.add_argument('-v','--version',help='Minecraft version of the mod', required=True)
arg_parser.add_argument('-s','--search',help='Number of the results returned by the search',type=int, default=5)
arg_parser.add_argument('-l','--latest',help='Autoselect latest release', action='store_true')

args = arg_parser.parse_args()

search_response = requests.get(f'https://api.modrinth.com/v2/search?query={args.name}&facets=[["project_type:mod"],["categories:{args.modloader}"],["versions:{args.version}"]]&limit={args.search}')
print(f'Status code: {search_response.status_code}')

search_json = search_response.json()

if search_json["total_hits"]:
    print("Search results: ")
    n=1
    for hit in search_json["hits"]:
        print(f'{n} - {hit["title"]} - {hit["description"]}')
        n = n + 1

    mod_select = int(input('Select a mod (eg "2"): ')) - 1 # Array indexes start at 0
    print(f'Selected mod: {search_json["hits"][mod_select]["title"]}')
    mod_id = search_json["hits"][mod_select]["project_id"]
    
    version_response = requests.get(f'https://api.modrinth.com/v2/project/{mod_id}/version?loaders=["{args.modloader}"]&game_versions=["{args.version}"]')
    print(f'Status code: {version_response.status_code}')

    version_json = version_response.json()

    if len(version_json): 
        if args.latest:
            print("Selecting latest release")
            release_select = 0;

        else:
            n = 1
            for version in version_json:
                print(f'{n} - {version["name"]}')
                n = n + 1

            release_select = int(input('Select a release (eg "2"): ')) - 1
        
        file_url = version_json[release_select]["files"][0]["url"]
        file_name = version_json[release_select]["files"][0]["filename"]
        print(f'Downloading file: {file_name}')

        file_response = requests.get(file_url)

        with open(file_name, "wb") as file:
            file.write(file_response.content)

    else:
        print("0 releases returned")

else:
    print("0 mods returned")
