from fastapi import FastAPI, HTTPException
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json import JSONDecodeError, loads
import uvicorn
import httpx

app = FastAPI()

# TODO: Put schema in a seprarate file
# jsonschema for validation. See: https://json-schema.org/specification.html
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
# Pass id to pokeAPI 
@app.get("/{id}")
async def root(id):
    async with httpx.AsyncClient() as client:
        try:
            # Fetch pokemon data:
            response = await client.get("https://pokeapi.co/api/v2/pokemon/{id}".format(id=id))
            pokemon = loads(response.text)
            validate(instance=pokemon, schema=pokemon_schema)
            # Fetch flavor:
            response = await client.get(pokemon["species"]["url"])
            species = loads(response.text)
            validate(instance=species, schema=species_schema)
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail="Could not fetch from PokeAPI")
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. not a valid JSON")
        except ValidationError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. schema validation failed")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Prepare for trouble, make it double! Meow, that's right!")
        
        
        result = {
            "id" : pokemon["id"],
            "name" : pokemon["name"],
            "image" : pokemon["sprites"]["front_default"],
            "type" : pokemon["types"][0]["type"]["name"], # Wasn't required but i think it's important.
            # I chose to show "blue" descriptions but in the future this can be changed
            "flavor_text": species["flavor_text_entries"][0]["flavor_text"]
        }
        return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)