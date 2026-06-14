import requests

search_query = "vulkan"
search_project = "mod"
search_limit = 5

search_response = requests.get(f'https://api.modrinth.com/v2/search?query={search_query}&facets=[["project_type:{search_project}"]]&limit={search_limit}')
print(f'Status code: {search_response.status_code}')

search_json = search_response.json()

if search_json["total_hits"] == 0:
    print("0 results returned")

else:
    n=1
    for hit in search_json["hits"]:
        print(f'{n}- {hit["title"]} - {hit["description"]}')
        n = n + 1

# mod_json = requests.get("https://api.modrinth.com/v2/project/JYQhtZtO").json()

# mod_name = mod_json["title"]
# mod_desc = mod_json["description"]

# print(f"Mod Name: {mod_name} \nMod Description: {mod_desc}")