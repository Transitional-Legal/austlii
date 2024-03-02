# ftc-chat-gpt-ai

## Python Notes

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
pip freeze > requirements.txt
```

```bash
# docker run --name redis-vecdb -d -p 6379:6379 -p 8001:8001 
docker-compose up
```

Run the api
```bash
# uvicorn main:app --reload
python -m flask --app api run
```