from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()


def fill_database(json_file='tests_data.json'):
    Base.metadata.create_all(engine)  # создаёт таблицы
    
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        fields = item['fields']
        if item['model'] == 'sale':
            fields['date_sale'] = datetime.strptime(fields['date_sale'], '%Y-%m-%d').date()
        
        if item['model'] == 'publisher':
            session.add(Publisher(id=item['pk'], **fields))
        elif item['model'] == 'book':
            session.add(Book(id=item['pk'], **fields))
        elif item['model'] == 'shop':
            session.add(Shop(id=item['pk'], **fields))
        elif item['model'] == 'stock':
            session.add(Stock(id=item['pk'], **fields))
        elif item['model'] == 'sale':
            session.add(Sale(id=item['pk'], **fields))

    session.commit()
    print("✅ База данных успешно заполнена!")


if __name__ == "__main__":
    fill_database()
