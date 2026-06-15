import csv
from pathlib import Path

PERCORSO_FILE_GREZZO = Path("dati/grezzi/shipments.csv")
PERCORSO_FILE_PULITO = Path("dati/elaborati/shipments_clean.csv")

INTESTAZIONI = [
    "shipment_id",
    "date",
    "station",
    "carrier",
    "route_id",
    "planned_departure",
    "actual_departure",
    "packages",
    "delivered_packages",
    "failed_packages",
    "late_minutes",
    "exception_type"
]

def leggi_spedizioni_grezze():
    spedizioni = []

    with open(PERCORSO_FILE_GREZZO, "r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)

        for riga in reader:
            spedizioni.append(riga)

    return spedizioni

def ha_campi_vuoti(riga):
    for valore in riga.values():
        if valore.strip() == "":
            return True

    return False

def converti_numeri(riga):
    riga["packages"] = int(riga["packages"])
    riga["delivered_packages"] = int(riga["delivered_packages"])
    riga["failed_packages"] = int(riga["failed_packages"])
    riga["late_minutes"] = int(riga["late_minutes"])

    return riga

def ha_numeri_negativi(riga):
    if riga["packages"] < 0:
        return True

    if riga["delivered_packages"] < 0:
        return True

    if riga["failed_packages"] < 0:
        return True

    if riga["late_minutes"] < 0:
        return True

    return False

def pacchi_coerenti(riga):
    totale_calcolato = riga["delivered_packages"] + riga["failed_packages"]

    if totale_calcolato == riga["packages"]:
        return True

    return False

def pulisci_spedizioni(spedizioni_grezze):
    spedizioni_pulite = []
    righe_scartate = 0

    for riga in spedizioni_grezze:
        if ha_campi_vuoti(riga):
            righe_scartate += 1
            continue

        riga = converti_numeri(riga)

        if ha_numeri_negativi(riga):
            righe_scartate += 1
            continue

        if not pacchi_coerenti(riga):
            righe_scartate += 1
            continue

        spedizioni_pulite.append(riga)

    return spedizioni_pulite, righe_scartate

def salva_spedizioni_pulite(spedizioni_pulite):
    with open(PERCORSO_FILE_PULITO, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=INTESTAZIONI)
        writer.writeheader()
        writer.writerows(spedizioni_pulite)

def crea_file_pulito():
    spedizioni_grezze = leggi_spedizioni_grezze()
    spedizioni_pulite, righe_scartate = pulisci_spedizioni(spedizioni_grezze)
    salva_spedizioni_pulite(spedizioni_pulite)

    return len(spedizioni_grezze), len(spedizioni_pulite), righe_scartate

if __name__ == "__main__":
    totale_grezze, totale_pulite, righe_scartate = crea_file_pulito()

    print("File shipments_clean.csv creato correttamente.")
    print("Spedizioni grezze:", totale_grezze)
    print("Spedizioni pulite:", totale_pulite)
    print("Righe scartate:", righe_scartate)

