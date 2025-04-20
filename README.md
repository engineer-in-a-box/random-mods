# How to use:
You need a file named `random-mods.json` in the same folder, this file contains 6 options:
* `username` (string): your factorio username
* `token` (string): your factorio token; this can be found in `player-data.json`, which is located in the [user data directory](https://wiki.factorio.com/Application_directory#User_data_directory)
* `version` (string): the version of factorio installed
* `mod_count` (integer): the length of the resulting mod list
* `has_space_age` (boolean): wether you have the space age expansion
* `mod_folder` (string): location of your mods folder relative to your user folder. ex: `"/AppData/Roaming/Factorio/mods"`

Example:
```json
{
    "username": "example-username",
    "token": "7a3f9c8e12b45d7f03ae6b9c4d8f21", 
    "version": "2.0",
    "mod_count": 50,
    "has_space_age": true,
    "mod_folder": "/AppData/Roaming/Factorio/mods"
}
```
