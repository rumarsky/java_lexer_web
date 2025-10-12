# Java Lexer Web (FastAPI)

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate  
# Windows: source .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
