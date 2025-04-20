import requests
import json
import random as rand
import regex as re
import math
import webbrowser
import os
import time
with open("random-mods.json", "r") as options_file:
    options = json.load(options_file)
    version = options["version"]
    mod_count = options["mod_count"]
    username = options["username"]
    token = options["token"]
    has_sa = options["has_space_age"]
    mod_folder = options["mod_folder"]
page_size = "max"
built_in_mods = {
    "space-age": False,
    "quality": False,
    "elevated-rails": False
}

table = json.loads(requests.get("https://mods.factorio.com/api/mods?hide_deprecated=true&page_size=%s&sort=updated_at&version=%s" % (page_size, version)).content)
mod_list = sorted(table["results"], key=lambda x: x["score"], reverse=True)

mod_list_final = []

def remove_duplicates(t):
    result = []
    for e in t:
        if e not in result:
            result.append(e)
    return result

def get_dependencies(mod_name):
    mod = json.loads(requests.get("https://mods.factorio.com/api/mods/%s/full" % mod_name).content)
    return mod["releases"][len(mod["releases"]) - 1]["info_json"]["dependencies"]

def add_mod(mod, is_dependency):
    if not "message" in mod:
        category = mod["category"] 
        if (category == "content") or is_dependency:
            print("Checking mod: %s" % mod["name"])
            incompats = []
            dependencies = []
            for depend in get_dependencies(mod["name"]):
                if depend[0] == "!":
                    incompats.append(re.sub("[1234567890<>=~?!(). ]", "", depend))
                if depend[0] == "~" or not re.match("[!?(]", depend):
                    dependencies.append(re.sub("[1234567890<>=~?!(). ]", "", depend))
            for depend in dependencies:
                if depend != "base" and depend != "space-age" and depend != "quality" and depend != "elevated-rails":
                    if not add_mod(json.loads(requests.get("https://mods.factorio.com/api/mods/%s" % re.sub("[1234567890<>=~?!(). ]", "", depend)).content), True):
                        print("Mod \"%s\" failed checks" % mod["name"])
                        return False
                elif has_sa and depend != "base":
                    if depend == "space-age":
                        built_in_mods["space-age"] = True
                    elif depend == "quality":
                        built_in_mods["quality"] = True
                    elif depend == "elevated-rails":
                        built_in_mods["elevated-rails"] = True
                else:
                    print("Mod \"%s\" failed checks" % mod["name"])
                    return False
            for incompat in incompats:
                for mod in mod_list_final:
                    if incompat == mod["name"]:
                        print("Mod \"%s\" failed checks" % mod["name"])
                        return False
            for mod2 in mod_list_final:
                for incompat in mod2["incompatabilities"]:
                    if incompat == mod["name"]:
                        print("Mod \"%s\" failed checks" % mod["name"])
                        return False
            if "releases" in mod:
                mod_list_final.append({
                    "name": mod["name"],
                    "incompatabilities": incompats,
                    "download": mod["releases"][len(mod["releases"]) - 1]["download_url"],
                    "version": mod["releases"][len(mod["releases"]) - 1]["version"]
                })
            elif "latest_release" in mod:
                mod_list_final.append({
                    "name": mod["name"],
                    "incompatabilities": incompats,
                    "download": mod["latest_release"]["download_url"],
                    "version": mod["latest_release"]["version"]
                })
                print("Mod \"%s\" passed checks" % mod["name"])
                return True
            else:
                print("Mod \"%s\" failed checks" % mod["name"])
                return False
        else:
            print("Mod \"%s\" failed checks" % mod["name"])
            return False
    else:
        print("Mod not found")
        return False

while len(mod_list_final) < mod_count:
    add_mod(mod_list[math.floor((rand.random() * math.sqrt(len(mod_list) - 1)) ** 2)], False)

mod_list_final = remove_duplicates(mod_list_final)

for mod in mod_list_final:
    print(mod["name"])

user_folder = "C:/users/%s" % os.getlogin()
mod_folder = user_folder + mod_folder
file_names = []

for mod in mod_list_final:
    webbrowser.open_new("https://mods.factorio.com%s?username=%s&token=%s" % (mod["download"], username, token))
    file_names.append("%s_%s.zip" % (mod["name"], mod["version"]))

time.sleep(mod_count * 3)

if built_in_mods["space-age"]:
    built_in_mods["quality"] = True
    built_in_mods["elevated-rails"] = True


for file_name in file_names:
    os.replace("%s/downloads/%s" % (user_folder, file_name), "%s/%s" % (mod_folder, file_name))

with open(mod_folder + "/mod-list.json", "r") as file:
    mod_list_json = json.load(file)
    for mod1 in mod_list_json["mods"]:
        for mod2 in mod_list_final:
            if mod1["name"] == mod2["name"] or mod1["name"] == "base" or (mod1["name"] in built_in_mods and built_in_mods[mod1["name"]]):
                mod1["enabled"] = True
            else:
                mod1["enabled"] = False
                
with open(mod_folder + "/mod-list.json", "w") as file:
    file.write(json.dumps(mod_list_json, indent = 2))