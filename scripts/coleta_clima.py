import requests
import mysql.connector
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY não encontrada. Verifique se o arquivo .env está na raiz do projeto.")

locais = [
    {"nome": "Natal", "lat": -5.79, "lon": -35.21},
    {"nome": "Parnamirim", "lat": -5.91, "lon": -35.26},
    {"nome": "Macaiba", "lat": -5.86, "lon": -35.35},
    {"nome": "Ceara Mirim", "lat": -5.64, "lon": -35.43},
    {"nome": "Sao Goncalo do Amarante", "lat": -5.79, "lon": -35.32},
    {"nome": "Mossoro", "lat": -5.19, "lon": -37.34},
    {"nome": "Caico", "lat": -6.46, "lon": -37.10},
    {"nome": "Pau dos Ferros", "lat": -6.11, "lon": -38.21}
]

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

def coletar_clima():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    for local in locais:
        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?lat={local['lat']}&lon={local['lon']}"
                f"&appid={API_KEY}&units=metric&lang=pt_br"
            )

            resposta = requests.get(url, timeout=30)

            if resposta.status_code != 200:
                print(f"Erro ao buscar dados de {local['nome']}: {resposta.text}")
                continue

            dados = resposta.json()

            cidade = local["nome"]
            latitude = local["lat"]
            longitude = local["lon"]

            temperatura = dados["main"]["temp"]
            umidade = dados["main"]["humidity"]
            descricao = dados["weather"][0]["description"]
            nuvens = dados["clouds"]["all"]

            chuva = 0.0
            if "rain" in dados and "1h" in dados["rain"]:
                chuva = float(dados["rain"]["1h"])

            data_coleta = datetime.utcnow() - timedelta(hours=3)

            sql = """
                INSERT INTO clima_dados
                (cidade, latitude, longitude, temperatura, descricao, chuva, data_coleta, umidade, nuvens)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                cidade,
                latitude,
                longitude,
                temperatura,
                descricao,
                chuva,
                data_coleta,
                umidade,
                nuvens
            )

            cursor.execute(sql, valores)
            conexao.commit()

            print(
                f"Salvo com sucesso: {cidade} | "
                f"Temp: {temperatura}°C | "
                f"Umidade: {umidade}% | "
                f"Nuvens: {nuvens}% | "
                f"Chuva: {chuva} mm"
            )

        except Exception as e:
            print(f"Erro geral em {local['nome']}: {e}")

    cursor.close()
    conexao.close()
    print("Coleta finalizada.")

if __name__ == "__main__":
    coletar_clima()