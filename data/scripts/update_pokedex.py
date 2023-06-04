import requests
import re
import json

data = requests.get(
    "https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/pokedex.ts"
).text

data = data.split("= {")
assert len(data) == 2, f"expecting data to have length=2: {[i[:50] for i in data]}"
data = "{" + data[1]

data = data.replace("\t", " ")

data = re.sub(r" +//.+", "", data)
data = re.sub(r"\/\*[\s\S]*?\*\/", "", data)

while "\n\n" in data:
    data = data.replace("\n\n", "\n")

data = re.sub(r",\n( *)([\}\]])", r"\n\1\2", data)

data = re.sub(r"([\w\d]+): ", r'"\1": ', data)

data = re.sub(r': ""(.*)":(.*)",', r': "\1:\2",', data)

data = data.replace("};", "}")

data_json = json.loads(data)

for k, v in data_json.items():
    v["baseStats"] = {
        "hp": v["baseStats"]["hp"],
        "attack": v["baseStats"]["atk"],
        "defense": v["baseStats"]["def"],
        "special-attack": v["baseStats"]["spa"],
        "special-defense": v["baseStats"]["spd"],
        "speed": v["baseStats"]["spe"],
    }
    v["types"] = [
        i.lower() for i in v["types"]
    ]
    v["name"] = v["name"].lower()

new_dict = {}
sorted_dex = sorted(data_json.items(), key=lambda x: x[1]["num"])
negative_nums = [i for i in sorted_dex if i[1]["num"] <= 0]
sorted_dex = [i for i in sorted_dex if i[1]["num"] > 0]
for k, v in sorted_dex + negative_nums:
    new_dict[k] = v

with open("pokedex_new.json", "w") as f:
    json.dump(data_json, f, indent=4)
