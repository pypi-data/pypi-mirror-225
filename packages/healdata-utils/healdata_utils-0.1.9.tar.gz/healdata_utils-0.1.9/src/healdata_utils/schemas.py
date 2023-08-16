import requests

jsonschema_url = (
    "https://raw.githubusercontent.com/norc-heal/"
    "heal-metadata-schemas/mbkranz/variable-lvl-dev/"
    "variable-level-metadata-schema/schemas/jsonschema/data-dictionary.json"
)
csvschema_url = (
    "https://raw.githubusercontent.com/norc-heal/heal-metadata-schemas/"
    "mbkranz/variable-lvl-dev/"
    "variable-level-metadata-schema/schemas/frictionless/csvtemplate/fields.json"
)

# TODO: install schemas from pip or make it a submodule (so no GET call necessary for fields.json)
healjsonschema = requests.get(jsonschema_url).json()
healcsvschema = requests.get(csvschema_url).json()
