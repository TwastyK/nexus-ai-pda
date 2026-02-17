import chromadb
# Замени в check_db.py
client = chromadb.PersistentClient(path="/data/vector_db")
collections = client.list_collections()

if collections:
    print("Доступные коллекции:")
    for col in collections:
        print(f"- {col.name}")
else:
    print("Коллекций не найдено. Проверь путь к vector_db.")