from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale
import os
from dotenv import load_dotenv

load_dotenv()

# === Настройки подключения ===
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()


def get_sales_by_publisher(publisher_name):
    result = session.query(
        Book.title,
        Shop.name,
        Sale.price,
        Sale.date_sale
    ).join(Publisher).join(Stock).join(Shop).join(Sale)\
     .filter(Publisher.name == publisher_name)\
     .order_by(Sale.date_sale.desc()).all()

    print(f"\n=== Продажи книг издателя '{publisher_name}' ===\n")
    for title, shop_name, price, date in result:
        print(f"{title} | {shop_name} | {price} | {date.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    name = input("Введите имя издателя (например: Пушкин): ").strip()
    if name:
        get_sales_by_publisher(name)
    else:
        print("Имя издателя не введено!")
