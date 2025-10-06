import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ===== KONFIGURACJA =====
csv_files = [
    ("RSS_FAR_70", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_FAR_70_log_of_B2K_WYRZUTNIA.csv"),
    ("RSS_FAR_49", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_FAR_49_log_of_B2K_WYRZUTNIA.csv"),
    ("RSS_FAR_28", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_FAR_28_log_of_B2K_WYRZUTNIA.csv"),
    ("RSS_FAR_00", r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program\Ships\Script\logs\RSS_FAR_00_log_of_B2K_WYRZUTNIA.csv"),
]

# --- STAŁE ---
S = 0.166  # powierzchnia przekroju rakiety [m²]
RHO_MIN = 1e-6  # dolny limit gęstości, żeby uniknąć dzielenia przez 0
V_MIN = 1.0     # dolny limit prędkości, żeby uniknąć dzielenia przez 0

# --- MAPOWANIE NAZW KOLUMN DO ŁADNYCH Etykiet ---
col_names_pretty = {
    'ALT': 'Altitude [m]',
    'LAT': 'Latitude [deg]',
    'LON': 'Longitude [deg]',
    'MASS': 'Mass [t]',
    'DYNPRESS': 'Dynamic Pressure [atm]',
    'BEARING': 'Bearing [deg]',
    'HEADING': 'Heading [deg]',
    'VERTSPEED': 'Vertical Speed [m/s]',
    'GROUNDSPEED': 'Ground Speed [m/s]',
    'ANGMOMX': 'Angular Momentum X [kg*m^2/s]',
    'ANGMOMY': 'Angular Momentum Y [kg*m^2/s]',
    'ANGMOMZ': 'Angular Momentum Z [kg*m^2/s]',
    'ANGVELX': 'Angular Velocity X [rad/s]',
    'ANGVELY': 'Angular Velocity Y [rad/s]',
    'ANGVELZ': 'Angular Velocity Z [rad/s]',
    'MACH': 'Mach Number [-]',
    'TEMP_K': 'Air Temperature [K]',
    'AIRDENS': 'Air Density [kg/m³]',
    'PRESS_PA': 'Static Pressure [Pa]',
    'THRUST': 'Vessel Thrust [N]'
}

def time_to_seconds(t):
    """Konwersja HH:MM:SS na sekundy"""
    h, m, s = map(int, t.split(':'))
    return h*3600 + m*60 + s

# ===== WCZYTANIE DANYCH =====
data = []
for label, path in csv_files:
    df = pd.read_csv(path, sep=';')
    df['TIME'] = df['TIME'].apply(time_to_seconds)
    
    # dynamic pressure w Pa (jeśli w atm)
    if df['DYNPRESS'].max() < 10:
        df['DYNPRESS_PA'] = df['DYNPRESS'] * 101325
    else:
        df['DYNPRESS_PA'] = df['DYNPRESS']

    # estymacja Cd
    df['Cd_est'] = df['DYNPRESS_PA'] / (
        0.5 * df['AIRDENS'].clip(lower=RHO_MIN) * (df['GROUNDSPEED'].clip(lower=V_MIN)**2) * S
    )

    data.append((label, df))

# ===== GENERACJA PDF =====
pdf_file = "RSS_flight_analysis_with_Cd_and_Thrust.pdf"
with PdfPages(pdf_file) as pdf:
    # wykresy 2D (TIME vs parametry)
    common_cols = [c for c in data[0][1].columns if c not in ['TIME', 'LAT', 'LON']]
    for col in common_cols:
        fig, ax = plt.subplots(figsize=(10, 4))
        for label, df in data:
            ax.plot(df['TIME'], df[col], label=label)
        ax.set_xlabel('Mission Time [s]')
        ax.set_ylabel(col_names_pretty.get(col, col))
        ax.set_title(f'{col_names_pretty.get(col, col)} vs Mission Time')
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    # Cd vs Mach
    for label, df in data:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(df['MACH'], df['Cd_est'], s=10, alpha=0.5)
        ax.set_xlabel('Mach [-]')
        ax.set_ylabel('Cd [-]')
        ax.set_title(f'{label}: Estimated Cd vs Mach')
        ax.grid(True)
        pdf.savefig(fig)
        plt.close(fig)

    # --- 3D trajektoria ---
    fig = plt.figure(figsize=(10, 7))
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
