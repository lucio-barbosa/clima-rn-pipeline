import os
import requests
from dotenv import load_dotenv

load_dotenv()

def enviar_telegram(mensagem=None):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não encontrados no .env")

    if mensagem is None:
        mensagem = """
🚨 ALERTA CLIMÁTICO RN

Sistema de alerta climático funcionando com sucesso.

✅ Telegram integrado
✅ Python conectado
✅ Projeto Clima RN operacional
"""

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": mensagem
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Alerta enviado com sucesso no Telegram!")
    else:
        print("❌ Erro ao enviar alerta.")
        print(response.text)

if __name__ == "__main__":
    enviar_telegram()