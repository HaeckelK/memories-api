# Memories API

Adding a memory:
```python
import requests

requests.post("http://localhost:5127/memories", data={"content": "That time I saw some movie."})
```

## Development

## Launching

## Database
Initial setup of database required:
```bash
docker-compose exec app bash
flask create-db
```
