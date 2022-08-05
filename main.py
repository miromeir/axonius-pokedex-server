from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import json

app = FastAPI()

# Pass id to pokeAPI 
@app.get("/{id}")
async def root(id):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get("https://pokeapi.co/api/v2/pokemon/{id}".format(id=id))
        except httpx.RequestError:
            raise HTTPException(status_code=400, detail="Not Found")
        else:
            pokemon = json.loads(r.text)
            return pokemon

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)