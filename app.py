import streamlit as st
from datetime import datetime, timedelta

# ----------------- FONCTION DE CALCUL -----------------
def options_programmation(
    heure_actuelle_str,
    duree_cycle_str,
    debut_fenetre_str,
    fin_fenetre_str,
    premier_increment_h=3,
    increment_suivant_h=1,
    max_increment_h=12
):
    now = datetime.strptime(heure_actuelle_str, "%H:%M")
    duree_cycle_parts = duree_cycle_str.split(":")
    duree_cycle = timedelta(hours=int(duree_cycle_parts[0]), minutes=int(duree_cycle_parts[1]))
    debut_fenetre = datetime.strptime(debut_fenetre_str, "%H:%M")
    fin_fenetre = datetime.strptime(fin_fenetre_str, "%H:%M")

    debut_fenetre = now.replace(hour=debut_fenetre.hour, minute=debut_fenetre.minute)
    fin_fenetre = now.replace(hour=fin_fenetre.hour, minute=fin_fenetre.minute)

    increments = [premier_increment_h + i * increment_suivant_h for i in range(max_increment_h)]
    solutions = []

    for inc in increments:
        fin_cycle = now + timedelta(hours=inc)
        debut_cycle = fin_cycle - duree_cycle
        if debut_fenetre <= debut_cycle and fin_cycle <= fin_fenetre:
            solutions.append({
                "increment_h": inc,
                "debut_cycle": debut_cycle.strftime("%H:%M"),
                "fin_cycle": fin_cycle.strftime("%H:%M")
            })

    return solutions

# ----------------- CONFIG PAGE -----------------
st.set_page_config(page_title="Programmateur Machine à Laver", page_icon="🧺", layout="wide")

# ----------------- CSS CUSTOM -----------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧺 Programmateur Machine à Laver")
st.write("Calcule automatiquement les **incréments de fin** qui respectent ta plage horaire.")

# ----------------- INIT SESSION STATE -----------------
if "heure_affichee" not in st.session_state:
    st.session_state.heure_affichee = datetime.now().time()
if "duree_cycle" not in st.session_state:
    st.session_state.duree_cycle = "1:40"
if "debut_fenetre" not in st.session_state:
    st.session_state.debut_fenetre = datetime.strptime("14:15", "%H:%M").time()
if "fin_fenetre" not in st.session_state:
    st.session_state.fin_fenetre = datetime.strptime("16:45", "%H:%M").time()

# ----------------- AFFICHAGE HEURE + RAFRAÎCHIR -----------------
col1, col2 = st.columns([2, 1])
with col1:
    st.time_input("⏰ Heure actuelle", value=st.session_state.heure_affichee, disabled=True)
with col2:
    if st.button("🔄 Rafraîchir l'heure"):
        st.session_state.heure_affichee = datetime.now().time()

# ----------------- FORMULAIRE -----------------
st.session_state.duree_cycle = st.text_input("⏳ Durée du cycle (H:MM)", value=st.session_state.duree_cycle)
st.session_state.debut_fenetre = st.time_input("🟢 Début de la fenêtre", value=st.session_state.debut_fenetre)
st.session_state.fin_fenetre = st.time_input("🔴 Fin de la fenêtre", value=st.session_state.fin_fenetre)

# ----------------- CALCUL -----------------
if st.button("📌 Calculer"):
    solutions = options_programmation(
        st.session_state.heure_affichee.strftime("%H:%M"),
        st.session_state.duree_cycle,
        st.session_state.debut_fenetre.strftime("%H:%M"),
        st.session_state.fin_fenetre.strftime("%H:%M")
    )

    st.markdown("---")
    if solutions:
        st.success("✅ Options possibles :")
        for s in solutions:
            st.markdown(f"- **+{s['increment_h']}h** → début `{s['debut_cycle']}` → fin `{s['fin_cycle']}`")
    else:
        st.error("❌ Aucune option trouvée dans la fenêtre donnée.")

