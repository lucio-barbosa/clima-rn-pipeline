import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def gerar_alertas_inteligentes():

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

    cursor = conexao.cursor(dictionary=True)

    query = """
    SELECT cd.*
    FROM clima_dados cd
    INNER JOIN (
        SELECT cidade, MAX(data_coleta) AS ultima_coleta
        FROM clima_dados
        GROUP BY cidade
    ) ult
        ON cd.cidade = ult.cidade
        AND cd.data_coleta = ult.ultima_coleta
    ORDER BY cd.cidade;
    """

    cursor.execute(query)
    dados = cursor.fetchall()

    mensagens = []

    for item in dados:
        cidade = item["cidade"]
        temperatura = item["temperatura"]
        umidade = item["umidade"]
        nuvens = item["nuvens"]
        chuva = item["chuva"]
        data_coleta = item["data_coleta"]

        
        if chuva >= 10:
            nivel = "🚨 ALERTA DE CHUVA INTENSA"
            recomendacao = "Evite áreas de alagamento e acompanhe os avisos oficiais."

        elif umidade >= 80 and nuvens >= 40:
            nivel = "⚠️ ALERTA MODERADO DE CHUVA"
            recomendacao = "Acompanhe a evolução do clima nas próximas horas."

        elif umidade <= 35 and chuva == 0:
            nivel = "☀️ ALERTA DE SECA SEVERA"
            recomendacao = "Economize água e evite exposição prolongada ao sol."

        elif umidade >= 85:
            nivel = "🌫️ ATENÇÃO: UMIDADE ELEVADA"
            recomendacao = "Umidade alta detectada. Acompanhe mudanças no tempo."

        elif nuvens >= 70:
            nivel = "☁️ ATENÇÃO: ALTA NEBULOSIDADE"
            recomendacao = "Céu muito nublado. Possibilidade de instabilidade climática."

        else:
            nivel = "🟢 SITUAÇÃO NORMAL"
            recomendacao = "Sem alerta crítico no momento."
            
        mensagem = f"""
{nivel}

📍 Cidade: {cidade}
🌡️ Temperatura: {temperatura}°C
💧 Umidade: {umidade}%
☁️ Nuvens: {nuvens}%
🌧️ Chuva: {chuva} mm
🕒 Coleta: {data_coleta}

ℹ️ Recomendação: {recomendacao}
"""
        mensagens.append(mensagem)

    cursor.close()
    conexao.close()

    mensagem_final = "\n".join(mensagens)

    print(mensagem_final)

    return mensagem_final


if __name__ == "__main__":
    gerar_alertas_inteligentes()