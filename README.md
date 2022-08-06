# axonius-pokedex-server

I used https://www.jsonschemavalidator.net/ for schema validation. 
Probably there's an extension for vscode.
In fact, most of my time was spent on creating a proper jsonschema.

Instructions:
```
git clone git@github.com:miromeir/axonius-pokedex-server.git
cd axonius-pokedex-server
```
Create & activate Virtual Env:
```
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Server is now up in http://localhost:8000 or http://127.0.0.1:8000
