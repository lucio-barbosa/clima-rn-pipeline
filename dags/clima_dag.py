from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append('/opt/airflow/project/scripts')

from coleta_clima import coletar_clima
from exporta_csv import exportar_csv
from exporta_excel import exportar_excel
from enviar_alerta_inteligente import enviar_alerta_inteligente_telegram

default_args = {
    "owner": "lucio",
    "start_date": datetime(2026, 5, 10),
    "retries": 1
}

with DAG(
    dag_id="clima_rn",
    default_args=default_args,
    schedule="0 * * * *",
    catchup=False,
    tags=["clima", "rn", "telegram", "csv", "excel"]
) as dag:

    tarefa_coleta = PythonOperator(
        task_id="coletar_clima",
        python_callable=coletar_clima
    )

    tarefa_exporta_csv = PythonOperator(
        task_id="exportar_csv",
        python_callable=exportar_csv
    )

    tarefa_exporta_excel = PythonOperator(
        task_id="exportar_excel",
        python_callable=exportar_excel
    )

    tarefa_alerta = PythonOperator(
        task_id="enviar_alerta_inteligente_telegram",
        python_callable=enviar_alerta_inteligente_telegram
    )

    tarefa_coleta >> tarefa_exporta_csv >> tarefa_exporta_excel >> tarefa_alerta