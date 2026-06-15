import csv
from pathlib import Path


PERCORSO_FILE_PULITO = Path("dati/elaborati/shipments_clean.csv")
PERCORSO_REPORT = Path("report/kpi_report.txt")
PERCORSO_KPI_GENERALI = Path("dati/elaborati/kpi_generali.csv")
PERCORSO_KPI_CARRIER = Path("dati/elaborati/kpi_carrier.csv")
PERCORSO_KPI_STATION = Path("dati/elaborati/kpi_station.csv")
PERCORSO_KPI_ANOMALIE = Path("dati/elaborati/kpi_anomalie.csv")


def leggi_spedizioni_pulite():
    spedizioni = []

    with open(PERCORSO_FILE_PULITO, "r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)

        for riga in reader:
            riga["packages"] = int(riga["packages"])
            riga["delivered_packages"] = int(riga["delivered_packages"])
            riga["failed_packages"] = int(riga["failed_packages"])
            riga["late_minutes"] = int(riga["late_minutes"])

            spedizioni.append(riga)

    return spedizioni


def calcola_kpi_generali(spedizioni):
    totale_spedizioni = len(spedizioni)

    totale_pacchi = 0
    totale_consegnati = 0
    totale_falliti = 0
    totale_ritardo = 0
    spedizioni_in_ritardo = 0

    for spedizione in spedizioni:
        totale_pacchi += spedizione["packages"]
        totale_consegnati += spedizione["delivered_packages"]
        totale_falliti += spedizione["failed_packages"]
        totale_ritardo += spedizione["late_minutes"]

        if spedizione["late_minutes"] > 0:
            spedizioni_in_ritardo += 1

    delivery_success_rate = round((totale_consegnati / totale_pacchi) * 100, 2)
    failed_delivery_rate = round((totale_falliti / totale_pacchi) * 100, 2)
    ritardo_medio = round(totale_ritardo / totale_spedizioni, 2)
    percentuale_spedizioni_in_ritardo = round((spedizioni_in_ritardo / totale_spedizioni) * 100, 2)

    return {
        "totale_spedizioni": totale_spedizioni,
        "totale_pacchi": totale_pacchi,
        "totale_pacchi_consegnati": totale_consegnati,
        "totale_pacchi_falliti": totale_falliti,
        "delivery_success_rate_percent": delivery_success_rate,
        "failed_delivery_rate_percent": failed_delivery_rate,
        "ritardo_medio_minuti": ritardo_medio,
        "spedizioni_in_ritardo": spedizioni_in_ritardo,
        "percentuale_spedizioni_in_ritardo": percentuale_spedizioni_in_ritardo
    }


def calcola_kpi_per_carrier(spedizioni):
    kpi_carrier = {}

    for spedizione in spedizioni:
        carrier = spedizione["carrier"]

        if carrier not in kpi_carrier:
            kpi_carrier[carrier] = {
                "totale_spedizioni": 0,
                "totale_pacchi": 0,
                "totale_consegnati": 0,
                "totale_falliti": 0,
                "totale_ritardo": 0
            }

        kpi_carrier[carrier]["totale_spedizioni"] += 1
        kpi_carrier[carrier]["totale_pacchi"] += spedizione["packages"]
        kpi_carrier[carrier]["totale_consegnati"] += spedizione["delivered_packages"]
        kpi_carrier[carrier]["totale_falliti"] += spedizione["failed_packages"]
        kpi_carrier[carrier]["totale_ritardo"] += spedizione["late_minutes"]

    for carrier, dati in kpi_carrier.items():
        dati["delivery_success_rate_percent"] = round(
            (dati["totale_consegnati"] / dati["totale_pacchi"]) * 100, 2
        )

        dati["failed_delivery_rate_percent"] = round(
            (dati["totale_falliti"] / dati["totale_pacchi"]) * 100, 2
        )

        dati["ritardo_medio_minuti"] = round(
            dati["totale_ritardo"] / dati["totale_spedizioni"], 2
        )

    return kpi_carrier


def calcola_kpi_per_station(spedizioni):
    kpi_station = {}

    for spedizione in spedizioni:
        station = spedizione["station"]

        if station not in kpi_station:
            kpi_station[station] = {
                "totale_spedizioni": 0,
                "totale_pacchi": 0,
                "totale_consegnati": 0,
                "totale_falliti": 0,
                "totale_ritardo": 0
            }

        kpi_station[station]["totale_spedizioni"] += 1
        kpi_station[station]["totale_pacchi"] += spedizione["packages"]
        kpi_station[station]["totale_consegnati"] += spedizione["delivered_packages"]
        kpi_station[station]["totale_falliti"] += spedizione["failed_packages"]
        kpi_station[station]["totale_ritardo"] += spedizione["late_minutes"]

    for station, dati in kpi_station.items():
        dati["delivery_success_rate_percent"] = round(
            (dati["totale_consegnati"] / dati["totale_pacchi"]) * 100, 2
        )

        dati["failed_delivery_rate_percent"] = round(
            (dati["totale_falliti"] / dati["totale_pacchi"]) * 100, 2
        )

        dati["ritardo_medio_minuti"] = round(
            dati["totale_ritardo"] / dati["totale_spedizioni"], 2
        )

    return kpi_station


def calcola_top_anomalie(spedizioni):
    anomalie = {}

    for spedizione in spedizioni:
        exception_type = spedizione["exception_type"]

        if exception_type not in anomalie:
            anomalie[exception_type] = 0

        anomalie[exception_type] += 1

    return anomalie


def calcola_tutti_i_kpi():
    spedizioni = leggi_spedizioni_pulite()

    kpi_generali = calcola_kpi_generali(spedizioni)
    kpi_carrier = calcola_kpi_per_carrier(spedizioni)
    kpi_station = calcola_kpi_per_station(spedizioni)
    top_anomalie = calcola_top_anomalie(spedizioni)

    return {
        "kpi_generali": kpi_generali,
        "kpi_carrier": kpi_carrier,
        "kpi_station": kpi_station,
        "top_anomalie": top_anomalie
    }


def genera_testo_report(risultati):
    kpi_generali = risultati["kpi_generali"]
    kpi_carrier = risultati["kpi_carrier"]
    kpi_station = risultati["kpi_station"]
    top_anomalie = risultati["top_anomalie"]

    testo = ""
    testo += "LOGISTICS OPERATIONS KPI REPORT\n"
    testo += "===============================\n\n"

    testo += "KPI GENERALI\n"
    testo += "------------\n"
    testo += f"Totale spedizioni: {kpi_generali['totale_spedizioni']}\n"
    testo += f"Totale pacchi: {kpi_generali['totale_pacchi']}\n"
    testo += f"Totale pacchi consegnati: {kpi_generali['totale_pacchi_consegnati']}\n"
    testo += f"Totale pacchi falliti: {kpi_generali['totale_pacchi_falliti']}\n"
    testo += f"Delivery success rate: {kpi_generali['delivery_success_rate_percent']}%\n"
    testo += f"Failed delivery rate: {kpi_generali['failed_delivery_rate_percent']}%\n"
    testo += f"Ritardo medio: {kpi_generali['ritardo_medio_minuti']} minuti\n"
    testo += f"Spedizioni in ritardo: {kpi_generali['spedizioni_in_ritardo']}\n"
    testo += f"Percentuale spedizioni in ritardo: {kpi_generali['percentuale_spedizioni_in_ritardo']}%\n\n"

    testo += "KPI PER CARRIER\n"
    testo += "---------------\n"

    for carrier, dati in kpi_carrier.items():
        testo += f"{carrier}\n"
        testo += f"  Totale spedizioni: {dati['totale_spedizioni']}\n"
        testo += f"  Totale pacchi: {dati['totale_pacchi']}\n"
        testo += f"  Delivery success rate: {dati['delivery_success_rate_percent']}%\n"
        testo += f"  Failed delivery rate: {dati['failed_delivery_rate_percent']}%\n"
        testo += f"  Ritardo medio: {dati['ritardo_medio_minuti']} minuti\n\n"

    testo += "KPI PER STATION\n"
    testo += "---------------\n"

    for station, dati in kpi_station.items():
        testo += f"{station}\n"
        testo += f"  Totale spedizioni: {dati['totale_spedizioni']}\n"
        testo += f"  Totale pacchi: {dati['totale_pacchi']}\n"
        testo += f"  Delivery success rate: {dati['delivery_success_rate_percent']}%\n"
        testo += f"  Failed delivery rate: {dati['failed_delivery_rate_percent']}%\n"
        testo += f"  Ritardo medio: {dati['ritardo_medio_minuti']} minuti\n\n"

    testo += "CONTEGGIO ANOMALIE\n"
    testo += "------------------\n"

    for anomalia, conteggio in top_anomalie.items():
        testo += f"{anomalia}: {conteggio}\n"

    return testo


def salva_report(testo_report):
    with open(PERCORSO_REPORT, "w", encoding="utf-8") as file_report:
        file_report.write(testo_report)

def salva_kpi_generali_csv(kpi_generali):
    with open(PERCORSO_KPI_GENERALI, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=kpi_generali.keys())
        writer.writeheader()
        writer.writerow(kpi_generali)

def salva_kpi_carrier_csv(kpi_carrier):
    intestazioni = [
        "carrier",
        "totale_spedizioni",
        "totale_pacchi",
        "totale_consegnati",
        "totale_falliti",
        "totale_ritardo",
        "delivery_success_rate_percent",
        "failed_delivery_rate_percent",
        "ritardo_medio_minuti"
    ]

    with open(PERCORSO_KPI_CARRIER, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=intestazioni)
        writer.writeheader()

        for carrier, dati in kpi_carrier.items():
            riga = {
                "carrier": carrier,
                "totale_spedizioni": dati["totale_spedizioni"],
                "totale_pacchi": dati["totale_pacchi"],
                "totale_consegnati": dati["totale_consegnati"],
                "totale_falliti": dati["totale_falliti"],
                "totale_ritardo": dati["totale_ritardo"],
                "delivery_success_rate_percent": dati["delivery_success_rate_percent"],
                "failed_delivery_rate_percent": dati["failed_delivery_rate_percent"],
                "ritardo_medio_minuti": dati["ritardo_medio_minuti"]
            }

            writer.writerow(riga)

def salva_kpi_station_csv(kpi_station):
    intestazioni = [
        "station",
        "totale_spedizioni",
        "totale_pacchi",
        "totale_consegnati",
        "totale_falliti",
        "totale_ritardo",
        "delivery_success_rate_percent",
        "failed_delivery_rate_percent",
        "ritardo_medio_minuti"
    ]

    with open(PERCORSO_KPI_STATION, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=intestazioni)
        writer.writeheader()

        for station, dati in kpi_station.items():
            riga = {
                "station": station,
                "totale_spedizioni": dati["totale_spedizioni"],
                "totale_pacchi": dati["totale_pacchi"],
                "totale_consegnati": dati["totale_consegnati"],
                "totale_falliti": dati["totale_falliti"],
                "totale_ritardo": dati["totale_ritardo"],
                "delivery_success_rate_percent": dati["delivery_success_rate_percent"],
                "failed_delivery_rate_percent": dati["failed_delivery_rate_percent"],
                "ritardo_medio_minuti": dati["ritardo_medio_minuti"]
            }

            writer.writerow(riga)

def salva_kpi_anomalie_csv(top_anomalie):
    intestazioni = [
        "exception_type",
        "conteggio"
    ]

    with open(PERCORSO_KPI_ANOMALIE, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=intestazioni)
        writer.writeheader()

        for anomalia, conteggio in top_anomalie.items():
            riga = {
                "exception_type": anomalia,
                "conteggio": conteggio
            }

            writer.writerow(riga)


def crea_report_kpi():
    risultati = calcola_tutti_i_kpi()

    testo_report = genera_testo_report(risultati)
    salva_report(testo_report)

    salva_kpi_generali_csv(risultati["kpi_generali"])

    salva_kpi_carrier_csv(risultati["kpi_carrier"])

    salva_kpi_station_csv(risultati["kpi_station"])

    salva_kpi_anomalie_csv(risultati["top_anomalie"])


if __name__ == "__main__":
    crea_report_kpi()
    print("Report KPI creato correttamente.")

