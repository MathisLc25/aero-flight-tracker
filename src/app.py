import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import math
from flight_engine import FLIGHTS_DATABASE, generate_flight_telemetry

st.set_page_config(
    page_title="Air France - Operations Control Center",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0B1325;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .af-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #002157;
        border-bottom: 3px solid #ED0000;
        padding: 12px 24px;
        border-radius: 6px;
        margin-bottom: 16px;
    }
    .af-brand {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 1.2px;
        color: #FFFFFF;
    }
    .af-badge-live {
        background-color: rgba(237, 0, 0, 0.2);
        border: 1px solid #ED0000;
        color: #FF4D4D;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
    }
    .af-card {
        background: #111C35;
        border: 1px solid #23355A;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .airport-big {
        font-size: 32px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
    }
    .airport-sub {
        font-size: 12px;
        color: #94A3B8;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 11px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="af-topbar">
    <div>
        <div class="af-brand">AIR FRANCE <span style="color:#ED0000;">/</span> OPS CONTROL CENTER</div>
        <div style="font-size: 11px; color: #94A3B8;">MONITORING TÉLÉMÉTRIQUE FLOTTE & MÉTÉO OPÉRATIONNELLE</div>
    </div>
    <div class="af-badge-live">RADAR ACTIF</div>
</div>
""", unsafe_allow_html=True)

flight_keys = list(FLIGHTS_DATABASE.keys())
selected_key = st.selectbox("Plan de vol sélectionné :", flight_keys, index=0)
flight, df = generate_flight_telemetry(selected_key)

st.markdown("##### Progression du vol en temps réel")
progress_pct = st.slider("Avancement du plan de vol (%) :", min_value=0, max_value=100, value=45, step=1)

idx = int((progress_pct / 100.0) * (len(df) - 1))
current_sample = df.iloc[idx]

angle_diff = math.radians(abs(flight["wind_dir"] - flight["rwy_heading"]))
crosswind = round(flight["wind_speed_kts"] * math.sin(angle_diff), 1)
headwind = round(flight["wind_speed_kts"] * math.cos(angle_diff), 1)

st.markdown(f"""
<div class="af-card" style="display: flex; justify-content: space-between; align-items: center;">
    <div>
        <div class="airport-big">{flight["dep_code"]}</div>
        <div class="airport-sub">{flight["dep_city"]} (CDG / LFPG)</div>
    </div>
    <div style="text-align: center;">
        <span style="color: #ED0000; font-size: 22px;">✈</span>
        <div style="font-size: 11px; color: #38BDF8; font-weight: 600;">{progress_pct}% PARCOURU</div>
    </div>
    <div style="text-align: right;">
        <div class="airport-big">{flight["arr_code"]}</div>
        <div class="airport-sub">{flight["arr_city"]}</div>
    </div>
    <div style="background: #1E2D4F; padding: 6px 14px; border-radius: 6px; border: 1px solid #2F4574;">
        <span style="font-weight: 700; color: #FFFFFF;">{flight["callsign"]}</span> &nbsp;|&nbsp; {flight["aircraft"]}
    </div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Altitude Courante", f"{current_sample['altitude_ft']:,.0f} ft", f"FL{int(current_sample['altitude_ft'] / 100)}")
k2.metric("Vitesse Sol (GS)", f"{current_sample['ground_speed_kts']:.0f} kts", f"M {current_sample['mach_number']}")
k3.metric("Cap Vrai (HDG)", f"{current_sample['bearing_deg']:.0f}°")
k4.metric("Variomètre (V/S)", f"{current_sample['vertical_speed_fpm']:+.0f} ft/min")
k5.metric("Carburant Brûlé", f"{current_sample['cumulative_fuel_kg'] / 1000.0:.1f} t")
co2_pax = (current_sample['cumulative_co2_kg'] / flight["pax_capacity"]) if flight["pax_capacity"] else 0
k6.metric("CO2 / Passager", f"{co2_pax:.0f} kg")

st.markdown("<br>", unsafe_allow_html=True)

col_map, col_details = st.columns([3, 2])

with col_map:
    st.markdown("##### Suivi Radar & Position Aéronef")
    start_pt = [df.iloc[0]["latitude"], df.iloc[0]["longitude"]]
    end_pt = [df.iloc[-1]["latitude"], df.iloc[-1]["longitude"]]
    cur_pt = [current_sample["latitude"], current_sample["longitude"]]

    dist = df['cumulative_dist_km'].iloc[-1]
    zoom = 2 if dist > 6000 else (4 if dist > 2000 else 6)

    m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=zoom, tiles="CartoDB dark_matter")

    coords_full = list(zip(df["latitude"], df["longitude"]))
    coords_traveled = list(zip(df.iloc[:idx+1]["latitude"], df.iloc[:idx+1]["longitude"]))

    folium.PolyLine(coords_full, color="#334155", weight=2, opacity=0.6).add_to(m)
    folium.PolyLine(coords_traveled, color="#ED0000", weight=4, opacity=0.9).add_to(m)

    folium.CircleMarker(start_pt, radius=5, color="#FFFFFF", fill=True, fill_color="#002157", popup="Origine: CDG").add_to(m)
    folium.CircleMarker(end_pt, radius=5, color="#FFFFFF", fill=True, fill_color="#ED0000", popup=f"Destination: {flight['arr_code']}").add_to(m)

    folium.Marker(
        cur_pt,
        popup=f"{flight['callsign']} - FL{int(current_sample['altitude_ft']/100)}",
        icon=folium.Icon(color="red", icon="plane", prefix="fa")
    ).add_to(m)

    st_folium(m, width="100%", height=490)

with col_details:
    st.markdown("##### Météo Opérationnelle & Vent Traversier (Arrivée)")
    cross_color = "#10B981" if crosswind < 20 else "#EF4444"
    st.markdown(f"""
    <div class="af-card">
        <div style="font-size: 13px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">AÉROPORT : {flight["arr_code"]} ({flight["arr_city"]})</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px;">
            <div>Piste en service : <b>RWY {flight["arr_rwy"]:02d}</b> (Axe {flight["rwy_heading"]}°)</div>
            <div>Vent mesuré : <b>{flight["wind_dir"]}° / {flight["wind_speed_kts"]} kts</b></div>
            <div>Vent de face / arrière : <b>{headwind:+.1f} kts</b></div>
            <div style="color: {cross_color};">Vent de travers : <b>{crosswind} kts</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### Profil de Vol & Position Actuelle")
    fig_alt = px.area(
        df,
        x="cumulative_dist_km",
        y="altitude_ft",
        labels={"cumulative_dist_km": "Distance (km)", "altitude_ft": "Altitude (ft)"},
        color_discrete_sequence=["#1E90FF"]
    )
    fig_alt.add_vline(x=current_sample["cumulative_dist_km"], line_dash="dash", line_color="#ED0000")
    fig_alt.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111C35",
        plot_bgcolor="#111C35",
        height=200,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_alt, use_container_width=True)