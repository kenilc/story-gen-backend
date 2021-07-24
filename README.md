This is the backend and frontend for a POC of story generation.

See also: ...

# Usage

Assume we have the trained model in the directory `./backend/models/checkpoint-final`.

## Backend

To start the server for testing:

```bash
> cd ./backend/
> pip install -r requirements.txt

> cat .env
CORS_ORIGINS=http://localhost:8000
MODEL_PATH=./models/checkpoint-final

> python app.py
```

To generate a story with title "On Sunday" and words "Tom", "breakfast", "park" and "bird":

```bash
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"title": "On Sunday", "storyline": ["Tom", "breakfast", "park", "bird"]}' \
  http://localhost:5000/api/v1/write
```

which will return (random output per run):

```json
[
  "Tom went to the park on Sunday.",
  "He enjoyed his breakfast.",
  "Tom was able to see two birds eating a clam.",
  "Tom went back to the car and got out of the park.",
  "The bird jumped out and began to eat."
]
```
