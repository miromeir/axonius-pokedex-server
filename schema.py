# Jsonschema for validation. 
# See: https://json-schema.org/specification.html
pokemon_schema = {
    "type" : "object",
    "properties": {
        "id" : {"type" : "number"},
        "name" : { "type":"string"},
        "types" : { "type":"array", 
                    "minItems":1,
                    "items":{
                        "type":"object",
                        "properties":{
                                        "type" : {
                                            "type": "object", 
                                            "properties": {
                                                "url":{"type": "string"}
                                            },
                                            "required":["url"]
                                        }
                                            
                                     },
                        "required":["type"]
                    }
                },
        "sprites" : { 
            "type" : "object",
            "properties" : {
                "front_default" : {"type" : "string"}
            },
            "required" : ["front_default"]
        },
        "species":{
            "type" : "object",
            "properties" : {
                "name" : {"type" : "string"},
                "url" : {"type" : "string"}
            },
            "required" : ["name","url"]
        }
    },
    "required":["name","types","id","sprites","species"]
}

species_schema = {
    "type" : "object",
    "properties": {
        "flavor_text_entries":{
            "type" : "array",
            "minItems": 1,
            "items" : {
                "type" : "object",
                "properties":{
                    "flavor_text":{"type":"string"}
                },
                "required" : ["flavor_text"]
            }
        }
    },
    "required":["flavor_text_entries"]
}