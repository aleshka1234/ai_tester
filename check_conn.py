from sqlalchemy import create_engine

# Сюда временно вставь свою строку
url = "postgresql://postgres:password@localhost:5432/ai_test_db"
engine = create_engine(url)

try:
    with engine.connect() as conn:
        print("✅ Соединение установлено! База данных отвечает.")
except Exception as e:
    print(f"❌ Ошибка: {e}")