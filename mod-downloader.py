import requests

search_query = "sodium"
search_loader= "fabric"
search_version = "1.21.1"
search_limit = 5
latest = False

search_response = requests.get(f'https://api.modrinth.com/v2/search?query={search_query}&facets=[["project_type:mod"],["categories:{search_loader}"],["versions:{search_version}"]]&limit={search_limit}')
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
    
    version_response = requests.get(f'https://api.modrinth.com/v2/project/{mod_id}/version?loaders=["{search_loader}"]&game_versions=["{search_version}"]')
    print(f'Status code: {version_response.status_code}')

    version_json = version_response.json()

    if len(version_json): 
        if latest:
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
