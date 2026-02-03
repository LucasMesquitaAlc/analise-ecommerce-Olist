import sqlite3
import pandas as pd
from pathlib import Path

#Criação dos caminhos
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "bruto"
DB_PATH = BASE_DIR / "olist.db"

#conecta-se ao db
conexao = sqlite3.connect(DB_PATH)

#mapeamento do nome da tabela para arquivo csv
tabelas = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

for tabela, arquivo in tabelas.items():
    caminho_csv = DATA_DIR / arquivo
    df = pd.read_csv(caminho_csv)

    df.to_sql(
        tabela,
        conexao,
        if_exists="replace",
        index=False
    )

    print(f"A tabela '{tabela}' foi atualizada e possui {len(df)} registros.")

conexao.close()

print("\nBanco atualizado")


# --testes--
cursor = conexao.cursor()

#1. listar tabelas
cursor.execute("""
    SELECT name 
    FROM sqlite_master 
    WHERE type='table';
""")
tabelas_db = [t[0] for t in cursor.fetchall()]

print("\nTabelas criadas:")
for t in tabelas_db:
    print("-", t)

#2.checar se há tabela vazia
for tabela in tabelas_db:
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    total = cursor.fetchone()[0]

    if total == 0:
        print(f"tabela '{tabela}' vazia!")
    else:
        print(f"{tabela}: {total} registros")