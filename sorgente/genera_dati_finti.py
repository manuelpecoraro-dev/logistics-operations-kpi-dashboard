import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

STAZIONI = [
    "ROMA_01",
    "ROMA_02",
    "MILANO_01",
    "NAPOLI_01",
    "BOLOGNA_01"
]

CARRIER = [
    "Carrier_A",
    "Carrier_B",
    "Carrier_C",
    "Carrier_D"
]

TIPI_ANOMALIA = [
    "none",
    "late_departure",
    "vehicle_issue",
    "missing_packages",
    "weather_delay",
    "address_issue",
    "customer_unavailable",
    "operational_delay"
]

ORARI_PARTENZA = [
    "08:00",
    "10:00",
    "12:00",
    "14:00",
    "16:00"
]

NUMERO_RIGHE = 300

PERCORSO_FILE_CSV = Path("dati/grezzi/shipments.csv")

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

def genera_shipment_id(numero):
    return "SHP" + f"{numero:04d}"

def genera_route_id(station):
    numero_route = random.randint(1, 10)
    return station + "_R" + f"{numero_route:03d}"

def genera_data_casuale():
    data_inizio = datetime(2026, 1, 1)
    giorni_da_aggiungere = random.randint(0, 30)
    data_generata = data_inizio + timedelta(days=giorni_da_aggiungere)
    return data_generata.strftime("%Y-%m-%d")

def calcola_orario_reale(orario_pianificato, minuti_ritardo):
    orario = datetime.strptime(orario_pianificato, "%H:%M")
    orario_reale = orario + timedelta(minutes=minuti_ritardo)
    return orario_reale.strftime("%H:%M")

def genera_pacchi():
    packages = random.randint(80, 220)
    failed_packages = random.randint(0, 10)
    delivered_packages = packages - failed_packages
    return packages, delivered_packages, failed_packages

def genera_minuti_ritardo():
    minuti_ritardo = random.randint(0, 45)
    return minuti_ritardo

def genera_tipo_anomalia():
    tipo_anomalia = random.choice(TIPI_ANOMALIA)
    return tipo_anomalia

def genera_spedizione(numero):
    shipment_id = genera_shipment_id(numero)
    data = genera_data_casuale()
    station = random.choice(STAZIONI)
    carrier = random.choice(CARRIER)
    route_id = genera_route_id(station)
    planned_departure = random.choice(ORARI_PARTENZA)
    late_minutes = genera_minuti_ritardo()
    actual_departure = calcola_orario_reale(planned_departure, late_minutes)
    packages, delivered_packages, failed_packages = genera_pacchi()
    exception_type = genera_tipo_anomalia()
    return shipment_id, data, station, carrier, route_id, planned_departure, actual_departure, packages, delivered_packages, failed_packages, late_minutes, exception_type

def genera_tutte_le_spedizioni():
    spedizioni = []

    for numero in range(1, NUMERO_RIGHE + 1):
        spedizione = genera_spedizione(numero)
        spedizioni.append(spedizione)

    return spedizioni

def salva_spedizioni_csv(spedizioni):
    with open(PERCORSO_FILE_CSV, "w", newline="", encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(INTESTAZIONI)
        writer.writerows(spedizioni)

def crea_file_shipments():
    random.seed(42)
    spedizioni = genera_tutte_le_spedizioni()
    salva_spedizioni_csv(spedizioni)

if __name__ == "__main__":
    crea_file_shipments()
    print("File shipments.csv creato correttamente.")




	





