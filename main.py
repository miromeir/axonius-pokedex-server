from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from jsonschema.exceptions import ValidationError
from schema import pokemon_schema, species_schema
from json import JSONDecodeError, loads
from jsonschema import validate
import uvicorn
import httpx

app = FastAPI()

# Pokemon ID for pokeAPI.
@app.get("/{id}")
async def root(id: int = Path(title="Pokemon ID for pokeAPI")):
    async with httpx.AsyncClient() as client:
        try:
            # Fetch pokemon: TODO: avoid hardcoded urls
            response = await client.get("https://pokeapi.co/api/v2/pokemon/{id}".format(id=id))
            pokemon = loads(response.text)
            # Validate jsonschema. See schema.py
            validate(instance=pokemon, schema=pokemon_schema)
            # Fetch flavor:
            response = await client.get(pokemon["species"]["url"]) # These indices are safe due to schema validation
            species = loads(response.text)
            # Validate jsonschema. See schema.py
            validate(instance=species, schema=species_schema)
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail="Could not fetch from PokeAPI")
        except JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. not a valid JSON")
        except ValidationError:
            raise HTTPException(status_code=400, detail="Error parsing data from pokeAPI. schema validation failed")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Prepare for trouble, make it double! Meow, that's right!")
        
        # Pick only the attributes we care about
        # The following indices are safe due to our schema validation
        result = {
            "id" : pokemon["id"],
            "name" : pokemon["name"],
            "image" : pokemon["sprites"]["front_default"],
            "type" : pokemon["types"][0]["type"]["name"], # Wasn't required but i think it's important.
            # I chose to show "blue" descriptions but in the future this can be changed
            # TODO: make sure language is "en"
            "flavor_text": species["flavor_text_entries"][0]["flavor_text"]
        }
        return result

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)