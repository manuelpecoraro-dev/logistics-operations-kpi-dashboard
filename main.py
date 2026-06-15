import subprocess
import sys

from sorgente.genera_dati_finti import crea_file_shipments
from sorgente.pulisci_dati import crea_file_pulito
from sorgente.calcola_kpi import crea_report_kpi


def esegui_pipeline():
    print("Starting Logistics Operations KPI Dashboard pipeline...")
    print("-" * 60)

    print("1. Generating synthetic shipment data...")
    crea_file_shipments()

    print("2. Cleaning and validating shipment data...")
    crea_file_pulito()

    print("3. Calculating operational KPIs and exporting CSV reports...")
    crea_report_kpi()

    print("4. Generating final HTML dashboard...")
    subprocess.run(
        [sys.executable, "sorgente/genera_dashboard_html.py"],
        check=True
    )

    print("-" * 60)
    print("Pipeline completed successfully.")
    print("Final dashboard:")
    print("report/dashboard_logistica.html")


if __name__ == "__main__":
    esegui_pipeline()
