from alerta_inteligente import gerar_alertas_inteligentes
from alerta_telegram import enviar_telegram

def enviar_alerta_inteligente_telegram():
    mensagem = gerar_alertas_inteligentes()
    enviar_telegram(mensagem)

if __name__ == "__main__":
    enviar_alerta_inteligente_telegram()