import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# ===== KONFIGURACJA =====
# lista (etykieta, ścieżka_do_pliku)
csv_files = [
    ("RSS_stock", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_stock_log_of_B2K_WYRZUTNIA.csv"),
    ("RSS_FAR", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_FAR_log_of_B2K_WYRZUTNIA.csv"),
]

# mapowanie ładnych nazw
col_names_pretty = {
    'ALT': 'Altitude [m]',
    'LAT': 'Latitude [deg]',
    'LON': 'Longitude [deg]',
    'MASS': 'Mass [t]',
    'DYNPRESS': 'Dynamic Pressure [ATM]',
    'BEARING': 'Bearing [deg]',
    'HEADING': 'Heading [deg]',
    'VERTSPEED': 'Vertical Speed [m/s]',
    'GROUNDSPEED': 'Ground Speed [m/s]',
    'ANGMOMX': 'Angular Momentum X [kg*m^2/s]',
    'ANGMOMY': 'Angular Momentum Y [kg*m^2/s]',
    'ANGMOMZ': 'Angular Momentum Z [kg*m^2/s]',
    'ANGVELX': 'Angular Velocity X [rad/s]',
    'ANGVELY': 'Angular Velocity Y [rad/s]',
    'ANGVELZ': 'Angular Velocity Z [rad/s]'
}

def time_to_seconds(t):
    h, m, s = map(int, t.split(':'))
    return h*3600 + m*60 + s

# ===== WCZYTANIE DANYCH =====
data = []
for label, path in csv_files:
    df = pd.read_csv(path, sep=';')
    df['TIME'] = df['TIME'].apply(time_to_seconds)
    data.append((label, df))

# kolumny (poza TIME) zakładamy, że są wspólne
common_cols = data[0][1].columns.tolist()
common_cols.remove('TIME')

# ===== GENERACJA PDF =====
pdf_file = "RSS_flight_analysis.pdf"
with PdfPages(pdf_file) as pdf:
    # --- wykresy 2D ---
    for col in common_cols:
        fig, ax = plt.subplots(figsize=(10,4))
        for label, df in data:
            ax.plot(df['TIME'], df[col],
                    label=f"{label}: {col_names_pretty.get(col, col)}")
        ax.set_xlabel('Mission Time [s]')
        ax.set_ylabel(col_names_pretty.get(col, col))
        ax.set_title(f'{col_names_pretty.get(col, col)} vs Mission Time')
        # ticki co 10 s w oparciu o max ze wszystkich plików
        max_time = max(d[1]['TIME'].max() for d in data)
        ax.set_xticks(np.arange(0, max_time + 50, 50))
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    # --- wykres 3D (trajektorie) ---
    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection='3d')
    for label, df in data:
        ax.plot(df['LON'], df['LAT'], df['ALT'], label=label)
    ax.set_xlabel('Longitude [deg]')
    ax.set_ylabel('Latitude [deg]')
    ax.set_zlabel('Altitude [m]')
    ax.set_title('3D Trajectory of Vessel')
    ax.legend()
    pdf.savefig(fig)
    plt.close(fig)

print(f"Wszystkie wykresy zapisane w pliku {pdf_file}")
