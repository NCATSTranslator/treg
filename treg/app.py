import json
import requests
import os
from biothings_explorer.smartapi_kg import MetaKG
from biothings_explorer.smartapi_kg.dataload import load_specs

def meta_kg ():
    kg = MetaKG()
    kg.constructMetaKG(source="remote")
    meta = kg.filter({"input_type": "Gene", "output_type": "ChemicalSubstance"})    
    print (json.dumps (meta, indent=2))

def get_specs ():
    specs = None
    specs_file = "specs.json"
    if os.path.exists (specs_file):
        with open (specs_file, "r") as stream:
            specs = json.load (stream)
    else:
        specs = load_specs (source="remote", tag="translator")
        #specs = requests.get ("https://smart-api.info/api/metakg").json ()
        with open("specs.json", "w") as stream:
            json.dump (specs, stream, indent=2)
    return specs

class DictX(dict):
    def __getattr__(self, key):
        result = None
        try:
            result = self[key]
        except KeyError as k:
            try:
                key = key.replace('_', '-')
                result = self[key]                
            except KeyError as k:
                raise AttributeError(k)
        if type(result) == dict:
            self[key] = DictX (result)
            result = self[key]
        return result
    
    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'

def set_default (d, key, default_value):
    if d.get (key) == None:
        d[key] = default_value

specs = get_specs ()
#xspecs = DictX (specs)
        
for api in specs: #specs.get("associations", []):
    api = DictX (api)
    set_default (api.info, "x-translator", {
        "team" : "",
        "component" : ""
    })
    set_default (api.info, "contact", {
        'email': '',
        'name': '',
        'x-id': '',
        'x-role': ''
    })
    set_default  (api, "servers", [
        {
            "description": "",
            "url" : ""
        }
    ])
    #print (f"{api}")
    
#    print (f"team:{api.info.x_translator.team} component: {api.info.x_translator.component} poc: {api.info.contact.email} name: {api.info.contact.get('name')} version: {api.info.version} url: {api._meta.url} servers: {api.servers}")
    print (f"team:{api.info.x_translator.team}")
    print (f"  component: {api.info.x_translator.component}")
    print (f"  poc      : {api.info.contact.email} name: {api.info.contact.get('name')}")
    print (f"  version  : {api.info.version} ")
    print (f"  url      : {api._meta.url} ")
    print (f"  servers  : {api.servers}")
