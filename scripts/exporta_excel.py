import mysql.connector
import pandas as pd
from datetime import datetime
import os

def exportar_excel():

    ambiente_airflow = os.path.exists("/opt/airflow")

    if ambiente_airflow:
        host = os.getenv("DB_HOST", "clima_mysql")
        port = int(os.getenv("DB_PORT", 3306))
    else:
        host = os.getenv("DB_HOST_LOCAL", "localhost")
        port = int(os.getenv("DB_PORT_LOCAL", 3307))

    conexao = mysql.connector.connect(
        host=host,
        port=port,
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin"),
        database=os.getenv("DB_NAME", "clima")
    )
    # =========================
    # CONSULTA SQL
    # =========================

    query = """
    SELECT
        id,
        cidade,
        latitude,
        longitude,
        temperatura,
        descricao,
        umidade,
        nuvens,
        chuva,
        data_coleta
    FROM clima_dados
    ORDER BY data_coleta DESC
    """

    # =========================
    # DATAFRAME
    # =========================

    df = pd.read_sql(query, conexao)

    # =========================
    # CRIAR PASTA DATA
    # =========================

    os.makedirs("data", exist_ok=True)

    # =========================
    # NOME DO ARQUIVO
    # =========================

    data_hoje = datetime.now().strftime("%Y-%m-%d")

    arquivo_excel = f"data/clima_{data_hoje}.xlsx"

    # =========================
    # EXPORTAÇÃO
    # =========================

    df.to_excel(arquivo_excel, index=False)

    # =========================
    # FINALIZAÇÃO
    # =========================

    print(f"✅ Arquivo Excel exportado com sucesso: {arquivo_excel}")

    conexao.close()


# =========================
# EXECUÇÃO MANUAL
# =========================

if __name__ == "__main__":
    exportar_excel()