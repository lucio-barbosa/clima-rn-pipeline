import os
from datetime import datetime
import mysql.connector
import pandas as pd

def conectar_banco():
    ambiente_airflow = os.path.exists("/opt/airflow")

    if ambiente_airflow:
        host = os.getenv("DB_HOST", "clima_mysql")
        port = int(os.getenv("DB_PORT", 3306))
    else:
        host = os.getenv("DB_HOST_LOCAL", "localhost")
        port = int(os.getenv("DB_PORT_LOCAL", 3307))

    return mysql.connector.connect(
        host=host,
        port=port,
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin"),
        database=os.getenv("DB_NAME", "clima")
    )

def exportar_csv():
    conexao = conectar_banco()

    query = """
        SELECT
            id,
            cidade,
            latitude,
            longitude,
            temperatura,
            descricao,
            chuva,
            data_coleta
        FROM clima_dados
        WHERE DATE(data_coleta) = CURDATE()
        ORDER BY cidade, data_coleta
    """

    df = pd.read_sql(query, conexao)
    conexao.close()

    os.makedirs("data", exist_ok=True)

    data_arquivo = datetime.now().strftime("%Y-%m-%d")
    caminho = f"data/clima_{data_arquivo}.csv"

    df.to_csv(caminho, index=False, encoding="utf-8-sig")

    print(f"CSV gerado com sucesso: {caminho}")

if __name__ == "__main__":
    exportar_csv()