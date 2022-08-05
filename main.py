from fastapi import FastAPI, HTTPException
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json import JSONDecodeError, loads
import uvicorn
import httpx

app = FastAPI()

# TODO: Put schema in a seprarate file
# jsonschema for validation. See: https://json-schema.org/specification.html
schema = {
    "type" : "object",
    "properties": {
        "id" : {"type" : "number"},
        "name" : { "type":"string"},
        "types" : { "type":"array", 
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
    "required":["name","types","id","sprites"]
}
# Pass id to pokeAPI 
@app.get("/{id}")
async def root(id):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://pokeapi.co/api/v2/pokemon/{id}".format(id=id))
            pokemon = loads(response.text)
            validate(instance=pokemon, schema=schema)
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail="Could not fetch from PokeAPI")
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. not a valid JSON")
        except ValidationError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. schema validation failed")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Prepare for trouble, make it double! Meow, that's right!")
        
        try:
            response = await client.get()
            
        result = {
            "id" : pokemon["id"],
            "name" : pokemon["name"],
            "image" : pokemon["sprites"]["front_default"]
        }
        return pokemon

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)