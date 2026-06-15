from pathlib import Path
import csv
import subprocess
import sys

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
DATI_DIR = BASE_DIR / "dati" / "elaborati"
REPORT_DIR = BASE_DIR / "report"
GRAFICI_DIR = REPORT_DIR / "grafici"

GRAFICI_DIR.mkdir(parents=True, exist_ok=True)


def leggi_csv(percorso):
    with open(percorso, mode="r", encoding="utf-8-sig", newline="") as file_csv:
        return list(csv.DictReader(file_csv))


def numero(valore):
    if valore is None:
        return 0

    testo = str(valore).strip().replace(",", ".")

    if testo == "":
        return 0

    return float(testo)


def format_intero(valore):
    return f"{int(round(numero(valore))):,}".replace(",", ".")


def format_decimale(valore, cifre=2):
    return f"{numero(valore):.{cifre}f}".replace(".", ",")


def format_percentuale(valore, cifre=1):
    return f"{numero(valore):.{cifre}f}%".replace(".", ",")


def pulisci_label(testo):
    return str(testo).replace("_", " ").title()


def prepara_grafico(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.grid(axis="x", alpha=0.18)
    ax.set_axisbelow(True)
    ax.tick_params(colors="#334155", labelsize=9)


def salva_barre_orizzontali(labels, values, xlabel, percorso, colore, suffix="", decimals=1):
    altezza = max(4.2, len(labels) * 0.58 + 1.2)

    fig, ax = plt.subplots(figsize=(10, altezza))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.barh(labels, values, color=colore)
    ax.invert_yaxis()

    prepara_grafico(ax)

    ax.set_xlabel(xlabel, fontsize=10, color="#334155")
    ax.set_ylabel("")

    massimo = max(values) if values else 0

    for posizione, valore in enumerate(values):
        if decimals == 0:
            testo = f"{int(round(valore))}{suffix}"
        else:
            testo = f"{valore:.1f}{suffix}"

        ax.text(
            valore + massimo * 0.015,
            posizione,
            testo,
            va="center",
            fontsize=9,
            color="#334155"
        )

    ax.set_xlim(0, massimo * 1.12)
    plt.tight_layout()
    plt.savefig(percorso, dpi=180, bbox_inches="tight")
    plt.close()


# =========================
# LETTURA DATI
# =========================

kpi_generali = leggi_csv(DATI_DIR / "kpi_generali.csv")[0]
kpi_station = leggi_csv(DATI_DIR / "kpi_station.csv")
kpi_carrier = leggi_csv(DATI_DIR / "kpi_carrier.csv")
kpi_anomalie = leggi_csv(DATI_DIR / "kpi_anomalie.csv")


# =========================
# KPI PRINCIPALI
# =========================

totale_spedizioni = format_intero(kpi_generali["totale_spedizioni"])
delivery_success_rate = format_percentuale(kpi_generali["delivery_success_rate_percent"])
ritardo_medio = format_decimale(kpi_generali["ritardo_medio_minuti"], 2)
pacchi_falliti = format_intero(kpi_generali["totale_pacchi_falliti"])


# =========================
# INSIGHT AUTOMATICI
# =========================

station_ordinate = sorted(
    kpi_station,
    key=lambda riga: numero(riga["ritardo_medio_minuti"]),
    reverse=True
)

station_peggiore = station_ordinate[0]["station"]
ritardo_station_peggiore = format_decimale(station_ordinate[0]["ritardo_medio_minuti"], 1)

anomalie_filtrate = [
    riga for riga in kpi_anomalie
    if riga["exception_type"].strip().lower() != "none"
]

anomalie_ordinate = sorted(
    anomalie_filtrate,
    key=lambda riga: numero(riga["conteggio"]),
    reverse=True
)

anomalia_principale = pulisci_label(anomalie_ordinate[0]["exception_type"])
conteggio_anomalia = format_intero(anomalie_ordinate[0]["conteggio"])

carrier_ordinati_failed = sorted(
    kpi_carrier,
    key=lambda riga: numero(riga["failed_delivery_rate_percent"]),
    reverse=True
)

carrier_critico = carrier_ordinati_failed[0]["carrier"]
failed_rate_carrier = format_percentuale(carrier_ordinati_failed[0]["failed_delivery_rate_percent"])


# =========================
# GRAFICI FINALI
# =========================

labels_station = [riga["station"] for riga in station_ordinate]
values_station = [numero(riga["ritardo_medio_minuti"]) for riga in station_ordinate]

salva_barre_orizzontali(
    labels_station,
    values_station,
    "Average delay (minutes)",
    GRAFICI_DIR / "ritardo_medio_station.png",
    colore="#2563EB",
    suffix=" min",
    decimals=1
)


labels_carrier = [riga["carrier"] for riga in carrier_ordinati_failed]
values_carrier = [numero(riga["failed_delivery_rate_percent"]) for riga in carrier_ordinati_failed]

salva_barre_orizzontali(
    labels_carrier,
    values_carrier,
    "Failed delivery rate (%)",
    GRAFICI_DIR / "failed_rate_carrier.png",
    colore="#F97316",
    suffix="%",
    decimals=1
)


labels_anomalie = [pulisci_label(riga["exception_type"]) for riga in anomalie_ordinate]
values_anomalie = [numero(riga["conteggio"]) for riga in anomalie_ordinate]

salva_barre_orizzontali(
    labels_anomalie,
    values_anomalie,
    "Number of occurrences",
    GRAFICI_DIR / "anomalie_principali.png",
    colore="#DC2626",
    suffix="",
    decimals=0
)


# =========================
# DASHBOARD HTML FINALE
# =========================

dashboard_path = REPORT_DIR / "dashboard_logistica.html"

html = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Logistics Operations KPI Dashboard</title>

    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #EEF3F8;
            font-family: Arial, sans-serif;
            color: #102A43;
        }}

        .page {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 34px 28px;
        }}

        .header {{
            background: linear-gradient(135deg, #0F172A, #1E293B);
            color: white;
            padding: 30px 32px;
            border-radius: 22px;
            margin-bottom: 22px;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
        }}

        .header h1 {{
            margin: 0 0 8px 0;
            font-size: 31px;
        }}

        .header p {{
            margin: 0;
            color: #D9E2EC;
            line-height: 1.5;
            max-width: 900px;
        }}

        .badge {{
            display: inline-block;
            background: #2563EB;
            color: white;
            padding: 6px 11px;
            border-radius: 999px;
            font-size: 12px;
            margin-bottom: 14px;
            letter-spacing: 0.2px;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 22px;
        }}

        .kpi-card {{
            background: white;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 8px 22px rgba(16, 42, 67, 0.08);
            border: 1px solid #D9E2EC;
        }}

        .kpi-card.blue {{
            border-top: 5px solid #2563EB;
        }}

        .kpi-card.green {{
            border-top: 5px solid #16A34A;
        }}

        .kpi-card.orange {{
            border-top: 5px solid #F97316;
        }}

        .kpi-card.red {{
            border-top: 5px solid #DC2626;
        }}

        .kpi-label {{
            font-size: 13px;
            color: #52616B;
            margin-bottom: 10px;
        }}

        .kpi-value {{
            font-size: 34px;
            font-weight: 700;
            color: #102A43;
        }}

        .kpi-note {{
            margin-top: 10px;
            font-size: 12px;
            color: #829AB1;
            line-height: 1.4;
        }}

        .insight-box {{
            background: white;
            border-radius: 18px;
            padding: 20px 24px;
            margin-bottom: 22px;
            box-shadow: 0 8px 22px rgba(16, 42, 67, 0.08);
            border-left: 6px solid #2563EB;
        }}

        .insight-box h2 {{
            margin-top: 0;
            font-size: 20px;
        }}

        .insight-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
        }}

        .insight {{
            background: #F4F7FB;
            border-radius: 14px;
            padding: 14px;
            font-size: 14px;
            line-height: 1.45;
        }}

        .section {{
            background: white;
            border-radius: 18px;
            padding: 22px 24px;
            margin-bottom: 22px;
            box-shadow: 0 8px 22px rgba(16, 42, 67, 0.08);
            border: 1px solid #D9E2EC;
        }}

        .section h2 {{
            margin-top: 0;
            margin-bottom: 6px;
            font-size: 22px;
        }}

        .section p {{
            color: #52616B;
            font-size: 14px;
            margin-top: 0;
            line-height: 1.5;
        }}

        .section img {{
            display: block;
            width: 100%;
            max-width: 980px;
            margin: 10px auto 0 auto;
        }}

        .footer {{
            color: #829AB1;
            font-size: 12px;
            text-align: center;
            margin-top: 28px;
        }}

        @media (max-width: 900px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .insight-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>
    <div class="page">

        <div class="header">
            <div class="badge">Python Data Pipeline Output</div>
            <h1>Logistics Operations KPI Dashboard</h1>
            <p>
                Operational dashboard generated through Python scripts from processed CSV files.
                The project simulates a data/operations pipeline to monitor shipments,
                logistics performance, delays, carriers and operational exceptions.
            </p>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card blue">
                <div class="kpi-label">Total shipments</div>
                <div class="kpi-value">{totale_spedizioni}</div>
                <div class="kpi-note">Total shipments analyzed in the dataset.</div>
            </div>

            <div class="kpi-card green">
                <div class="kpi-label">Delivery success rate</div>
                <div class="kpi-value">{delivery_success_rate}</div>
                <div class="kpi-note">Percentage of packages delivered successfully.</div>
            </div>

            <div class="kpi-card orange">
                <div class="kpi-label">Average delay</div>
                <div class="kpi-value">{ritardo_medio} min</div>
                <div class="kpi-note">Average delay rilevato sulle spedizioni.</div>
            </div>

            <div class="kpi-card red">
                <div class="kpi-label">Failed packages</div>
                <div class="kpi-value">{pacchi_falliti}</div>
                <div class="kpi-note">Packages not delivered successfully.</div>
            </div>
        </div>

        <div class="insight-box">
            <h2>Operational insights</h2>
            <div class="insight-grid">
                <div class="insight">
                    <b>Highest-delay station:</b><br>
                    {station_peggiore} with {ritardo_station_peggiore} minutes average delay.
                </div>

                <div class="insight">
                    <b>Top exception type:</b><br>
                    {anomalia_principale} with {conteggio_anomalia} occurrences.
                </div>

                <div class="insight">
                    <b>Carrier to monitor:</b><br>
                    {carrier_critico} with a failed delivery rate of {failed_rate_carrier}.
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Average delay per station</h2>
            <p>
                Comparison of stations by average operational delay.
                Useful for identifying areas that may require deeper investigation.
            </p>
            <img src="grafici/ritardo_medio_station.png" alt="Average delay per station">
        </div>

        <div class="section">
            <h2>Failed delivery rate per carrier</h2>
            <p>
                Comparison of carriers by failed package percentage.
                This metric is easier to read than success rate when carrier performance is very similar.
            </p>
            <img src="grafici/failed_rate_carrier.png" alt="Failed delivery rate per carrier">
        </div>

        <div class="section">
            <h2>Main operational exceptions</h2>
            <p>
                Distribution of the main operational exceptions, excluding records with no exception.
                The chart helps identify the most frequent issues impacting the process.
            </p>
            <img src="grafici/anomalie_principali.png" alt="Main operational exceptions">
        </div>

        <div class="footer">
            Generated with Python from processed CSV files — Logistics KPI Portfolio Project
        </div>

    </div>
</body>
</html>
"""

dashboard_path.write_text(html, encoding="utf-8")

print("Final dashboard generated successfully:")
print(dashboard_path)
