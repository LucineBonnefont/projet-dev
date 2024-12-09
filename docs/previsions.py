import pandas as pd
import holidays
import calendar
from bike_data import get_bike_data, get_bike_routes
from density import create_density_map, generate_map
from collections import defaultdict

# Fonction pour calculer la densité pour le jour suivant (J+1)
def predict_density(current_date):
    """
    Prédit la densité du trafic pour le jour suivant basé sur les conditions suivantes :
    - Formule 1 : Année non bissextile et jour non férié.
    - Formule 2 : Année non bissextile et jour férié.
    - Formule 3 : Année bissextile et jour non férié.
    - Formule 4 : Année bissextile et jour férié.
    
    :param current_date: La date actuelle pour laquelle la densité doit être prédite (format 'YYYY-MM-DD')
    :return: La carte de densité prédite pour le jour suivant (J+1)
    """
    current_date = pd.to_datetime(current_date)
    year = current_date.year

    # Vérifier si le jour suivant est un jour férié
    france_holidays = holidays.France()
    is_holiday = (current_date + pd.Timedelta(days=1)) in france_holidays
    is_leap = calendar.isleap(year)

    # Récupération des données nécessaires
    month = current_date.month
    prev_month_2 = month - 2 if month > 2 else month + 10
    prev_year = year - 1 if month > 2 else year - 2

    # Nombre de vélos utilisés pour le mois M-2 de l'année en cours et précédente
    data = pd.read_csv('data/TAM_MMM_CoursesVelomagg.csv', low_memory=False)
    data['Departure'] = pd.to_datetime(data['Departure'])
    data['Return'] = pd.to_datetime(data['Return'])
    bikes_month_m2_a = data[
        (data['Departure'].dt.month == prev_month_2) & (data['Departure'].dt.year == year) |
        (data['Return'].dt.month == prev_month_2) & (data['Return'].dt.year == year)
    ].shape[0]
    bikes_month_m2_a1 = data[
        (data['Departure'].dt.month == prev_month_2) & (data['Departure'].dt.year == prev_year) |
        (data['Return'].dt.month == prev_month_2) & (data['Return'].dt.year == prev_year)
    ].shape[0]

    if bikes_month_m2_a1 == 0:
        raise ValueError(f"Données manquantes pour les vélos utilisés en {prev_month_2}/{prev_year}.")

    # Ratio des vélos utilisés
    bike_ratio = bikes_month_m2_a / bikes_month_m2_a1

    # Extraire les densités des jours J, J+1, J+2, J+3, J-1 de l'année précédente
    date_last_year = current_date.replace(year=prev_year)
    dates_to_analyze = {
        "density_j": date_last_year,
        "density_j_plus_1": date_last_year + pd.Timedelta(days=1),
        "density_j_plus_2": date_last_year + pd.Timedelta(days=2),
        "density_j_plus_3": date_last_year + pd.Timedelta(days=3),
        "density_j_minus_1": date_last_year - pd.Timedelta(days=1)
    }

    frequencies = dict()
    for name, date_to_analyze in dates_to_analyze.items():
        stations, trajets = get_bike_data(date_to_analyze)
        bikes_routes = get_bike_routes(stations, trajets)
        segment_frequency = create_density_map(bikes_routes, return_frequency=True)
        frequencies[name] = segment_frequency

    # Récupérer tous les segments uniques de routes
    unique_segments = set()
    for day_segments in frequencies.values():
        unique_segments.update(day_segments.keys())

    # Déterminer les prévisions sur chaque segment pour le lendemain
    segment_frequency = defaultdict(int)


    for segment in unique_segments:

        density_j_plus_1 = frequencies["density_j_plus_1"][segment]
        density_j_plus_2 = frequencies["density_j_plus_2"][segment]
        density_j_plus_3 = frequencies["density_j_plus_3"][segment]
        density_j = frequencies["density_j"][segment]
        density_j_minus_1 = frequencies["density_j_minus_1"][segment]

         # Appliquer la formule selon les conditions
        if not is_leap and not is_holiday:
            # Formule pour année non bissextile et jour non férié
            predicted_density = bike_ratio * (
                0.5 * density_j_plus_1 +
                0.3 * density_j +
                0.1 * density_j_plus_2 +
                0.1 * density_j_minus_1
            )
        elif not is_leap and is_holiday:
            # Formule pour année non bissextile et jour férié
            predicted_density = bike_ratio * (
                0.2 * density_j_plus_1 +
                0.6 * density_j +
                0.1 * density_j_plus_2 +
                0.1 * density_j_minus_1
            )
        elif is_leap and not is_holiday:
            # Formule pour année bissextile et jour non férié
            predicted_density = bike_ratio * (
                0.5 * density_j_plus_2 +
                0.3 * density_j_plus_1 +
                0.1 * density_j_plus_3 +
                0.1 * density_j
            )
        elif is_leap and is_holiday:
            # Formule pour année bissextile et jour férié
            predicted_density = bike_ratio * (
                0.1 * density_j_plus_1 +
                0.6 * density_j +
                0.2 * density_j_plus_2 +
                0.1 * density_j_minus_1
            )
        else:
            raise ValueError("Cas non traité.")
        
        segment_frequency[segment] = predicted_density

    return generate_map(segment_frequency)

