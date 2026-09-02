import pandas as pd
import numpy as np
from geopy.distance import geodesic
import math

FLIGHTS_DATABASE = {
    "AF7620 (CDG -> BOD)": {
        "callsign": "AFR7620",
        "aircraft": "Airbus A320-200",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "BOD", "arr_city": "Bordeaux",
        "arr_rwy": 23, "rwy_heading": 230, "wind_dir": 260, "wind_speed_kts": 14,
        "max_fl": 280, "burn_climb": 45.0, "burn_cruise": 32.0, "pax_capacity": 178,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 48.3500, "lon": 1.9500, "alt_ft": 16000, "speed_kts": 320},
            {"lat": 47.1000, "lon": 1.1000, "alt_ft": 28000, "speed_kts": 430},
            {"lat": 45.8500, "lon": 0.2000, "alt_ft": 14000, "speed_kts": 290},
            {"lat": 44.8283, "lon": -0.7156, "alt_ft": 0, "speed_kts": 135}
        ]
    },
    "AF1240 (CDG -> AMS)": {
        "callsign": "AFR1240",
        "aircraft": "Airbus A220-300",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "AMS", "arr_city": "Amsterdam",
        "arr_rwy": 18, "rwy_heading": 184, "wind_dir": 210, "wind_speed_kts": 18,
        "max_fl": 260, "burn_climb": 38.0, "burn_cruise": 26.0, "pax_capacity": 148,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 49.9500, "lon": 2.9000, "alt_ft": 18000, "speed_kts": 340},
            {"lat": 51.1000, "lon": 3.7000, "alt_ft": 26000, "speed_kts": 410},
            {"lat": 51.8500, "lon": 4.4000, "alt_ft": 9000, "speed_kts": 260},
            {"lat": 52.3105, "lon": 4.7683, "alt_ft": 0, "speed_kts": 130}
        ]
    },
    "AF0090 (CDG -> MIA)": {
        "callsign": "AFR090",
        "aircraft": "Boeing 777-300ER",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "MIA", "arr_city": "Miami",
        "arr_rwy": 9, "rwy_heading": 92, "wind_dir": 120, "wind_speed_kts": 12,
        "max_fl": 380, "burn_climb": 110.0, "burn_cruise": 84.0, "pax_capacity": 381,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 50.8000, "lon": -4.2000, "alt_ft": 24000, "speed_kts": 410},
            {"lat": 49.5000, "lon": -20.0000, "alt_ft": 36000, "speed_kts": 485},
            {"lat": 42.0000, "lon": -45.0000, "alt_ft": 38000, "speed_kts": 490},
            {"lat": 32.0000, "lon": -68.0000, "alt_ft": 38000, "speed_kts": 490},
            {"lat": 27.5000, "lon": -77.5000, "alt_ft": 19000, "speed_kts": 360},
            {"lat": 25.7959, "lon": -80.2870, "alt_ft": 0, "speed_kts": 140}
        ]
    },
    "AF0096 (CDG -> MCO)": {
        "callsign": "AFR096",
        "aircraft": "Airbus A350-900",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "MCO", "arr_city": "Orlando",
        "arr_rwy": 18, "rwy_heading": 185, "wind_dir": 160, "wind_speed_kts": 10,
        "max_fl": 390, "burn_climb": 95.0, "burn_cruise": 72.0, "pax_capacity": 324,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 51.0000, "lon": -5.0000, "alt_ft": 25000, "speed_kts": 420},
            {"lat": 50.2000, "lon": -22.0000, "alt_ft": 37000, "speed_kts": 485},
            {"lat": 43.5000, "lon": -46.0000, "alt_ft": 39000, "speed_kts": 490},
            {"lat": 34.0000, "lon": -69.0000, "alt_ft": 39000, "speed_kts": 490},
            {"lat": 30.0000, "lon": -78.5000, "alt_ft": 18000, "speed_kts": 350},
            {"lat": 28.4312, "lon": -81.3081, "alt_ft": 0, "speed_kts": 138}
        ]
    },
    "AF0084 (CDG -> SFO)": {
        "callsign": "AFR084",
        "aircraft": "Boeing 777-300ER",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "SFO", "arr_city": "San Francisco",
        "arr_rwy": 28, "rwy_heading": 284, "wind_dir": 310, "wind_speed_kts": 16,
        "max_fl": 380, "burn_climb": 115.0, "burn_cruise": 88.0, "pax_capacity": 381,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 56.0000, "lon": -8.0000, "alt_ft": 28000, "speed_kts": 430},
            {"lat": 64.0000, "lon": -35.0000, "alt_ft": 36000, "speed_kts": 480},
            {"lat": 65.0000, "lon": -60.0000, "alt_ft": 38000, "speed_kts": 485},
            {"lat": 58.0000, "lon": -95.0000, "alt_ft": 38000, "speed_kts": 490},
            {"lat": 48.0000, "lon": -115.0000, "alt_ft": 38000, "speed_kts": 490},
            {"lat": 40.0000, "lon": -120.0000, "alt_ft": 16000, "speed_kts": 340},
            {"lat": 37.6213, "lon": -122.3790, "alt_ft": 0, "speed_kts": 140}
        ]
    },
    "AF0650 (CDG -> CUN)": {
        "callsign": "AFR650",
        "aircraft": "Boeing 777-300ER",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "CUN", "arr_city": "Cancun",
        "arr_rwy": 12, "rwy_heading": 125, "wind_dir": 90, "wind_speed_kts": 11,
        "max_fl": 370, "burn_climb": 112.0, "burn_cruise": 86.0, "pax_capacity": 468,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 48.5000, "lon": -7.0000, "alt_ft": 26000, "speed_kts": 420},
            {"lat": 44.0000, "lon": -25.0000, "alt_ft": 36000, "speed_kts": 485},
            {"lat": 35.0000, "lon": -50.0000, "alt_ft": 37000, "speed_kts": 490},
            {"lat": 26.5000, "lon": -74.0000, "alt_ft": 37000, "speed_kts": 490},
            {"lat": 22.5000, "lon": -83.5000, "alt_ft": 17000, "speed_kts": 350},
            {"lat": 21.0365, "lon": -86.8771, "alt_ft": 0, "speed_kts": 138}
        ]
    },
    "AF0842 (CDG -> FDF)": {
        "callsign": "AFR842",
        "aircraft": "Boeing 777-300ER",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "FDF", "arr_city": "Fort-de-France",
        "arr_rwy": 10, "rwy_heading": 97, "wind_dir": 80, "wind_speed_kts": 15,
        "max_fl": 370, "burn_climb": 108.0, "burn_cruise": 82.0, "pax_capacity": 468,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 46.5000, "lon": -6.0000, "alt_ft": 26000, "speed_kts": 420},
            {"lat": 38.0000, "lon": -24.0000, "alt_ft": 35000, "speed_kts": 485},
            {"lat": 28.0000, "lon": -42.0000, "alt_ft": 37000, "speed_kts": 490},
            {"lat": 19.5000, "lon": -56.0000, "alt_ft": 37000, "speed_kts": 490},
            {"lat": 15.5000, "lon": -60.0000, "alt_ft": 12000, "speed_kts": 290},
            {"lat": 14.5910, "lon": -61.0025, "alt_ft": 0, "speed_kts": 135}
        ]
    },
    "AF0792 (CDG -> PTP)": {
        "callsign": "AFR792",
        "aircraft": "Airbus A350-900",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "PTP", "arr_city": "Pointe-a-Pitre",
        "arr_rwy": 12, "rwy_heading": 115, "wind_dir": 90, "wind_speed_kts": 14,
        "max_fl": 390, "burn_climb": 92.0, "burn_cruise": 70.0, "pax_capacity": 324,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 47.0000, "lon": -5.5000, "alt_ft": 27000, "speed_kts": 430},
            {"lat": 39.5000, "lon": -23.0000, "alt_ft": 37000, "speed_kts": 485},
            {"lat": 29.5000, "lon": -41.0000, "alt_ft": 39000, "speed_kts": 490},
            {"lat": 21.0000, "lon": -55.0000, "alt_ft": 39000, "speed_kts": 490},
            {"lat": 17.0000, "lon": -60.5000, "alt_ft": 14000, "speed_kts": 300},
            {"lat": 16.2653, "lon": -61.5318, "alt_ft": 0, "speed_kts": 136}
        ]
    },
    "AF0276 (CDG -> HND)": {
        "callsign": "AFR276",
        "aircraft": "Airbus A350-900",
        "dep_code": "CDG", "dep_city": "Paris", "arr_code": "HND", "arr_city": "Tokyo",
        "arr_rwy": 34, "rwy_heading": 337, "wind_dir": 360, "wind_speed_kts": 12,
        "max_fl": 410, "burn_climb": 98.0, "burn_cruise": 74.0, "pax_capacity": 324,
        "waypoints": [
            {"lat": 49.0097, "lon": 2.5479, "alt_ft": 0, "speed_kts": 0},
            {"lat": 45.0000, "lon": 20.0000, "alt_ft": 28000, "speed_kts": 430},
            {"lat": 39.0000, "lon": 42.0000, "alt_ft": 37000, "speed_kts": 485},
            {"lat": 32.0000, "lon": 65.0000, "alt_ft": 39000, "speed_kts": 490},
            {"lat": 28.0000, "lon": 90.0000, "alt_ft": 41000, "speed_kts": 490},
            {"lat": 31.0000, "lon": 115.0000, "alt_ft": 41000, "speed_kts": 490},
            {"lat": 33.5000, "lon": 133.0000, "alt_ft": 22000, "speed_kts": 380},
            {"lat": 35.5494, "lon": 139.7798, "alt_ft": 0, "speed_kts": 142}
        ]
    }
}

def calculate_bearing(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    bearing = math.degrees(math.atan2(y, x))
    return (bearing + 360) % 360

def generate_flight_telemetry(flight_key, total_samples=120):
    flight = FLIGHTS_DATABASE[flight_key]
    waypoints = flight["waypoints"]
    segs = len(waypoints) - 1
    pts_per_seg = max(2, total_samples // segs)

    lats, lons, alts, speeds = [], [], [], []

    for i in range(segs):
        p1, p2 = waypoints[i], waypoints[i+1]
        lats.extend(np.linspace(p1["lat"], p2["lat"], pts_per_seg))
        lons.extend(np.linspace(p1["lon"], p2["lon"], pts_per_seg))
        alts.extend(np.linspace(p1["alt_ft"], p2["alt_ft"], pts_per_seg))
        speeds.extend(np.linspace(p1["speed_kts"], p2["speed_kts"], pts_per_seg))

    df = pd.DataFrame({
        "latitude": lats,
        "longitude": lons,
        "altitude_ft": alts,
        "ground_speed_kts": speeds
    })

    distances, bearings, vertical_speeds = [0.0], [0.0], [0.0]

    for i in range(1, len(df)):
        p_prev = (df.iloc[i-1]["latitude"], df.iloc[i-1]["longitude"])
        p_curr = (df.iloc[i]["latitude"], df.iloc[i]["longitude"])
        d_km = geodesic(p_prev, p_curr).kilometers
        distances.append(d_km)

        brng = calculate_bearing(p_prev[0], p_prev[1], p_curr[0], p_curr[1])
        bearings.append(brng)

        delta_alt = df.iloc[i]["altitude_ft"] - df.iloc[i-1]["altitude_ft"]
        vs = (delta_alt / 1.5)
        vertical_speeds.append(vs)

    df["segment_dist_km"] = distances
    df["cumulative_dist_km"] = df["segment_dist_km"].cumsum()
    df["bearing_deg"] = bearings
    df["vertical_speed_fpm"] = vertical_speeds
    df["mach_number"] = (df["ground_speed_kts"] / 573.8).round(2)

    rate = np.where(df["altitude_ft"] < 25000, flight["burn_climb"], flight["burn_cruise"])
    burn_step = (rate * (df["segment_dist_km"] / (df["ground_speed_kts"].replace(0, 1) * 1.852)) * 60).fillna(0)
    df["cumulative_fuel_kg"] = burn_step.cumsum()
    df["cumulative_co2_kg"] = df["cumulative_fuel_kg"] * 3.16

    return flight, df