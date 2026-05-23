import random

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="GeoQuiz Mundial",
    page_icon="🌍",
    layout="wide",
)

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════
COUNTRIES = {
    "Afganistán":       {"capital": "Kabul",                     "iso": "AFG"},
    "Albania":          {"capital": "Tirana",                    "iso": "ALB"},
    "Alemania":         {"capital": "Berlín",                    "iso": "DEU"},
    "Angola":           {"capital": "Luanda",                    "iso": "AGO"},
    "Arabia Saudita":   {"capital": "Riad",                      "iso": "SAU"},
    "Argelia":          {"capital": "Argel",                     "iso": "DZA"},
    "Argentina":        {"capital": "Buenos Aires",              "iso": "ARG"},
    "Australia":        {"capital": "Canberra",                  "iso": "AUS"},
    "Austria":          {"capital": "Viena",                     "iso": "AUT"},
    "Bangladesh":       {"capital": "Daca",                      "iso": "BGD"},
    "Bélgica":          {"capital": "Bruselas",                  "iso": "BEL"},
    "Bolivia":          {"capital": "Sucre",                     "iso": "BOL"},
    "Brasil":           {"capital": "Brasilia",                  "iso": "BRA"},
    "Camboya":          {"capital": "Nom Pen",                   "iso": "KHM"},
    "Camerún":          {"capital": "Yaundé",                    "iso": "CMR"},
    "Canadá":           {"capital": "Ottawa",                    "iso": "CAN"},
    "Chile":            {"capital": "Santiago",                  "iso": "CHL"},
    "China":            {"capital": "Pekín",                     "iso": "CHN"},
    "Colombia":         {"capital": "Bogotá",                    "iso": "COL"},
    "Corea del Norte":  {"capital": "Pionyang",                  "iso": "PRK"},
    "Corea del Sur":    {"capital": "Seúl",                      "iso": "KOR"},
    "Costa Rica":       {"capital": "San José",                  "iso": "CRI"},
    "Cuba":             {"capital": "La Habana",                 "iso": "CUB"},
    "Dinamarca":        {"capital": "Copenhague",                "iso": "DNK"},
    "Ecuador":          {"capital": "Quito",                     "iso": "ECU"},
    "Egipto":           {"capital": "El Cairo",                  "iso": "EGY"},
    "España":           {"capital": "Madrid",                    "iso": "ESP"},
    "Etiopía":          {"capital": "Adís Abeba",                "iso": "ETH"},
    "Filipinas":        {"capital": "Manila",                    "iso": "PHL"},
    "Finlandia":        {"capital": "Helsinki",                  "iso": "FIN"},
    "Francia":          {"capital": "París",                     "iso": "FRA"},
    "Ghana":            {"capital": "Acra",                      "iso": "GHA"},
    "Grecia":           {"capital": "Atenas",                    "iso": "GRC"},
    "Guatemala":        {"capital": "Ciudad de Guatemala",       "iso": "GTM"},
    "Honduras":         {"capital": "Tegucigalpa",               "iso": "HND"},
    "Hungría":          {"capital": "Budapest",                  "iso": "HUN"},
    "India":            {"capital": "Nueva Delhi",               "iso": "IND"},
    "Indonesia":        {"capital": "Yakarta",                   "iso": "IDN"},
    "Irak":             {"capital": "Bagdad",                    "iso": "IRQ"},
    "Irán":             {"capital": "Teherán",                   "iso": "IRN"},
    "Irlanda":          {"capital": "Dublín",                    "iso": "IRL"},
    "Israel":           {"capital": "Jerusalén",                 "iso": "ISR"},
    "Italia":           {"capital": "Roma",                      "iso": "ITA"},
    "Japón":            {"capital": "Tokio",                     "iso": "JPN"},
    "Jordania":         {"capital": "Ammán",                     "iso": "JOR"},
    "Kenia":            {"capital": "Nairobi",                   "iso": "KEN"},
    "Libia":            {"capital": "Trípoli",                   "iso": "LBY"},
    "Malasia":          {"capital": "Kuala Lumpur",              "iso": "MYS"},
    "Marruecos":        {"capital": "Rabat",                     "iso": "MAR"},
    "México":           {"capital": "Ciudad de México",          "iso": "MEX"},
    "Mozambique":       {"capital": "Maputo",                    "iso": "MOZ"},
    "Myanmar":          {"capital": "Naipyidó",                  "iso": "MMR"},
    "Nepal":            {"capital": "Katmandú",                  "iso": "NPL"},
    "Nicaragua":        {"capital": "Managua",                   "iso": "NIC"},
    "Nigeria":          {"capital": "Abuja",                     "iso": "NGA"},
    "Noruega":          {"capital": "Oslo",                      "iso": "NOR"},
    "Nueva Zelanda":    {"capital": "Wellington",                "iso": "NZL"},
    "Países Bajos":     {"capital": "Ámsterdam",                 "iso": "NLD"},
    "Pakistán":         {"capital": "Islamabad",                 "iso": "PAK"},
    "Panamá":           {"capital": "Ciudad de Panamá",          "iso": "PAN"},
    "Paraguay":         {"capital": "Asunción",                  "iso": "PRY"},
    "Perú":             {"capital": "Lima",                      "iso": "PER"},
    "Polonia":          {"capital": "Varsovia",                  "iso": "POL"},
    "Portugal":         {"capital": "Lisboa",                    "iso": "PRT"},
    "Reino Unido":      {"capital": "Londres",                   "iso": "GBR"},
    "República Checa":  {"capital": "Praga",                     "iso": "CZE"},
    "Rumania":          {"capital": "Bucarest",                  "iso": "ROU"},
    "Rusia":            {"capital": "Moscú",                     "iso": "RUS"},
    "Siria":            {"capital": "Damasco",                   "iso": "SYR"},
    "Somalia":          {"capital": "Mogadiscio",                "iso": "SOM"},
    "Sri Lanka":        {"capital": "Sri Jayawardenepura Kotte", "iso": "LKA"},
    "Sudáfrica":        {"capital": "Pretoria",                  "iso": "ZAF"},
    "Sudán":            {"capital": "Jartum",                    "iso": "SDN"},
    "Suecia":           {"capital": "Estocolmo",                 "iso": "SWE"},
    "Suiza":            {"capital": "Berna",                     "iso": "CHE"},
    "Tailandia":        {"capital": "Bangkok",                   "iso": "THA"},
    "Tanzania":         {"capital": "Dodoma",                    "iso": "TZA"},
    "Turquía":          {"capital": "Ankara",                    "iso": "TUR"},
    "Ucrania":          {"capital": "Kiev",                      "iso": "UKR"},
    "Uganda":           {"capital": "Kampala",                   "iso": "UGA"},
    "Uruguay":          {"capital": "Montevideo",                "iso": "URY"},
    "Uzbekistán":       {"capital": "Taskent",                   "iso": "UZB"},
    "Venezuela":        {"capital": "Caracas",                   "iso": "VEN"},
    "Vietnam":          {"capital": "Hanói",                     "iso": "VNM"},
    "Yemen":            {"capital": "Saná",                      "iso": "YEM"},
    "Zimbabue":         {"capital": "Harare",                    "iso": "ZWE"},
}

COUNTRY_NAMES = list(COUNTRIES.keys())

# ════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════
_DEFAULTS = {
    "score": 0,
    "total": 0,
    "streak": 0,
    "best_streak": 0,
    "q_idx": 0,
    "question": None,
    "mode": None,
    "options": [],
    "answered": False,
    "result": None,
    "chosen_cap": None,
    "clicked_iso": None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════
def new_question(mode):
    country = random.choice(COUNTRY_NAMES)
    st.session_state.update(
        question=country,
        mode=mode,
        answered=False,
        result=None,
        chosen_cap=None,
        clicked_iso=None,
        q_idx=st.session_state.q_idx + 1,
    )
    if mode == "capital":
        correct = COUNTRIES[country]["capital"]
        pool = [COUNTRIES[c]["capital"] for c in COUNTRIES if c != country]
        opts = [correct] + random.sample(pool, 3)
        random.shuffle(opts)
        st.session_state.options = opts


def record_answer(correct, clicked_iso=None):
    if st.session_state.answered:
        return
    st.session_state.answered = True
    st.session_state.total += 1
    st.session_state.clicked_iso = clicked_iso
    if correct:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.best_streak = max(
            st.session_state.best_streak, st.session_state.streak
        )
        st.session_state.result = "correct"
    else:
        st.session_state.streak = 0
        st.session_state.result = "wrong"


def build_map(highlight_correct=None, highlight_wrong=None):
    rows = [
        {
            "iso": d["iso"],
            "nombre": name,
            "val": (
                2 if d["iso"] == highlight_correct
                else 0 if d["iso"] == highlight_wrong
                else 1
            ),
        }
        for name, d in COUNTRIES.items()
    ]
    df = pd.DataFrame(rows)
    fig = px.choropleth(
        df,
        locations="iso",
        locationmode="ISO-3",
        color="val",
        hover_name="nombre",
        color_continuous_scale=["#e74c3c", "#3498db", "#2ecc71"],
        range_color=[0, 2],
    )
    fig.update_layout(
        coloraxis_showscale=False,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        height=440,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
            landcolor="#c8d8e8",
            oceancolor="#aec6cf",
            showocean=True,
            coastlinecolor="#888",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><extra></extra>",
        marker_line_color="white",
        marker_line_width=0.5,
    )
    return fig


# ════════════════════════════════════════════════════════════════
# UI — HEADER
# ════════════════════════════════════════════════════════════════
st.title("🌍 GeoQuiz Mundial")
st.caption(f"Pon a prueba tus conocimientos de geografía · {len(COUNTRY_NAMES)} países disponibles")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Puntuación", st.session_state.score)
m2.metric("Racha 🔥", st.session_state.streak)
m3.metric("Mejor racha 🏆", st.session_state.best_streak)
_acc = (
    f"{st.session_state.score / st.session_state.total * 100:.0f}%"
    if st.session_state.total else "—"
)
m4.metric("Precisión", _acc)

st.divider()

# ── CONTROLS ─────────────────────────────────────────────────────
b1, b2, b3, b4 = st.columns([1.3, 1.6, 0.9, 0.9])
if b1.button("🗺️ Señalar país", use_container_width=True):
    new_question("map")
    st.rerun()
if b2.button("🏛️ ¿Cuál es la capital?", use_container_width=True):
    new_question("capital")
    st.rerun()
if st.session_state.question:
    if b3.button("⏭️ Siguiente", use_container_width=True):
        new_question(st.session_state.mode)
        st.rerun()
    if b4.button("🔄 Reiniciar", use_container_width=True):
        for k, v in _DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

st.divider()

# ════════════════════════════════════════════════════════════════
# UI — PANTALLA DE BIENVENIDA
# ════════════════════════════════════════════════════════════════
if not st.session_state.question:
    st.markdown("## 👆 Elige un modo de juego para comenzar")
    col_i1, col_i2 = st.columns(2)
    col_i1.info(
        "**🗺️ Señalar país** – Se nombra un país y debes hacer clic "
        "sobre él en el mapa mundial."
    )
    col_i2.info(
        "**🏛️ Capital** – Se nombra un país y debes elegir "
        "su capital entre 4 opciones."
    )
    st.plotly_chart(build_map(), use_container_width=True, key="welcome_map")
    st.stop()

# ════════════════════════════════════════════════════════════════
# UI — QUIZ
# ════════════════════════════════════════════════════════════════
country = st.session_state.question
mode = st.session_state.mode
correct_iso = COUNTRIES[country]["iso"]
q_idx = st.session_state.q_idx

# ── MODO MAPA ────────────────────────────────────────────────────
if mode == "map":
    st.subheader(f"🗺️ ¿Dónde está **{country}**?")
    if not st.session_state.answered:
        st.caption("Haz clic directamente sobre el país en el mapa.")

    if st.session_state.answered:
        wrong = st.session_state.clicked_iso
        fig = build_map(
            highlight_correct=correct_iso,
            highlight_wrong=wrong if wrong and wrong != correct_iso else None,
        )
    else:
        fig = build_map()

    ev = st.plotly_chart(
        fig,
        on_select="rerun",
        use_container_width=True,
        key=f"map_q_{q_idx}",
    )

    if not st.session_state.answered and ev and ev.selection and ev.selection.points:
        iso_clicked = ev.selection.points[0].get("location")
        if iso_clicked:
            record_answer(iso_clicked == correct_iso, clicked_iso=iso_clicked)
            st.rerun()

# ── MODO CAPITAL ──────────────────────────────────────────────────
elif mode == "capital":
    left, right = st.columns([2, 3])

    with left:
        st.subheader(f"🏛️ ¿Cuál es la capital de **{country}**?")
        st.caption("El país está resaltado en azul en el mapa.")
        st.write("")

        correct_cap = COUNTRIES[country]["capital"]
        btn_cols = st.columns(2)
        for i, opt in enumerate(st.session_state.options):
            with btn_cols[i % 2]:
                if not st.session_state.answered:
                    if st.button(opt, use_container_width=True, key=f"opt_{q_idx}_{i}"):
                        st.session_state.chosen_cap = opt
                        record_answer(opt == correct_cap)
                        st.rerun()
                else:
                    if opt == correct_cap:
                        st.success(f"✓ {opt}")
                    elif opt == st.session_state.chosen_cap:
                        st.error(f"✗ {opt}")
                    else:
                        st.button(opt, disabled=True, key=f"opt_dis_{q_idx}_{i}")

    with right:
        st.plotly_chart(
            build_map(highlight_correct=correct_iso),
            use_container_width=True,
            key=f"cap_map_{q_idx}",
        )

# ── FEEDBACK ─────────────────────────────────────────────────────
if st.session_state.result == "correct":
    st.success("✅ ¡Correcto! 🎉")
elif st.session_state.result == "wrong":
    if mode == "capital":
        st.error(
            f"❌ Incorrecto. La capital de **{country}** es "
            f"**{COUNTRIES[country]['capital']}**."
        )
    else:
        st.error(
            f"❌ Incorrecto. **{country}** aparece resaltado en **verde** en el mapa."
        )

