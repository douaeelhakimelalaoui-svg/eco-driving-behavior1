import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Chargement du modèle
model = joblib.load('model_conduite.pkl')

# Titre
st.title("🚗 Système de recommandation éco-responsable")
st.markdown("---")

# Explication de l'IA
with st.expander("ℹ️ Comment fonctionne l'IA ?"):
    st.write("""
    Ce système utilise un algorithme **Random Forest** entraîné sur 
    30 000 trajets réels. Il analyse votre comportement de conduite 
    et prédit votre consommation énergétique en L/100km.
    
    **Variables analysées :**
    - RPM variation : instabilité du régime moteur
    - Freinages brusques : nombre d'arrêts brutaux
    - Temps au ralenti : moteur allumé sans avancer
    - Fluidité d'accélération : douceur de conduite (0 à 1)
    - Eco score : score global de conduite (0 à 100)
    """)

st.subheader("📊 Entrez votre comportement de conduite :")

col1, col2 = st.columns(2)

with col1:
    rpm = st.slider("Variation RPM", 500, 5000, 1800,
                    help="Instabilité du régime moteur — plus c'est bas, mieux c'est")
    harsh_braking = st.slider("Freinages brusques", 0, 15, 3,
                    help="Nombre de freinages brutaux pendant le trajet")
    idling = st.slider("Temps au ralenti (min)", 0, 33, 10,
                    help="Durée moteur allumé sans avancer")

with col2:
    smoothness = st.slider("Fluidité d'accélération", 0.0, 1.0, 0.7,
                    help="0 = très brusque, 1 = très fluide")
    eco_score = st.slider("Eco Score", 0, 100, 50,
                    help="Score global de conduite éco-responsable")

# Prédiction
if st.button("🔍 Analyser ma conduite"):

    entree = [[rpm, harsh_braking, idling, smoothness, eco_score]]
    prediction = model.predict(entree)[0]

    # Score éco
    if prediction < 6:
        score = "A 🟢"
    elif prediction < 8:
        score = "B 🟡"
    else:
        score = "C 🔴"

    st.markdown("---")
    st.markdown(f"### ⛽ Consommation estimée : **{round(prediction, 2)} L/100km**")
    st.markdown(f"### 🏆 Score éco-conduite : **{score}**")
    st.markdown("---")

    # Recommandations
    st.markdown("### 💡 Recommandations :")

    # RPM
    st.markdown("#### 🔧 Régime moteur (RPM) :")
    st.info("📌 Un régime optimal se situe entre 1000 et 2500 RPM")
    if rpm > 3000:
        st.error(f"❌ RPM trop élevé ({rpm}) — passez à la vitesse supérieure")
    elif rpm > 2500:
        st.warning(f"⚠️ RPM élevé ({rpm}) — conduisez plus régulièrement")
    else:
        st.success(f"✅ RPM correct ({rpm}) — bon régime moteur")

    # Freinages brusques
    st.markdown("#### 🛑 Freinages brusques :")
    st.info("📌 Freiner brusquement = énergie perdue + usure des freins")
    if harsh_braking > 5:
        st.error(f"❌ {harsh_braking} freinages brusques — anticipez mieux les obstacles")
    elif harsh_braking > 2:
        st.warning(f"⚠️ {harsh_braking} freinages brusques — essayez de réduire")
    else:
        st.success(f"✅ {harsh_braking} freinages brusques — excellente anticipation")

    # Temps au ralenti
    st.markdown("#### ⏱️ Temps au ralenti :")
    st.info("📌 Le moteur au ralenti consomme du carburant inutilement")
    if idling > 15:
        st.error(f"❌ {idling} min au ralenti — coupez le moteur si arrêt > 1 min")
    elif idling > 8:
        st.warning(f"⚠️ {idling} min au ralenti — réduisez les arrêts moteur allumé")
    else:
        st.success(f"✅ {idling} min au ralenti — très bien")

    # Fluidité d'accélération
    st.markdown("#### ⚡ Fluidité d'accélération :")
    st.info("📌 Une accélération fluide réduit la consommation de 10 à 30%")
    if smoothness < 0.4:
        st.error(f"❌ Accélération très brusque ({smoothness}) — accélérez progressivement")
    elif smoothness < 0.6:
        st.warning(f"⚠️ Accélération moyenne ({smoothness}) — peut mieux faire")
    else:
        st.success(f"✅ Accélération fluide ({smoothness}) — excellente conduite")

    # Eco Score
    st.markdown("#### 🌿 Eco Score :")
    st.info("📌 Score global calculé sur l'ensemble de votre comportement de conduite")
    if eco_score < 30:
        st.error(f"❌ Score faible ({eco_score}/100) — conduite très énergivore")
    elif eco_score < 60:
        st.warning(f"⚠️ Score moyen ({eco_score}/100) — des améliorations sont possibles")
    else:
        st.success(f"✅ Bon score ({eco_score}/100) — conduite éco-responsable")

    # Bilan global
    st.markdown("---")
    st.markdown("#### 📊 Bilan global :")
    if prediction < 6:
        st.success("✅ Excellente conduite éco-responsable !")
    elif prediction < 8:
        st.info("ℹ️ Conduite correcte — quelques ajustements possibles")
    else:
        st.error("❌ Consommation élevée — suivez les recommandations ci-dessus")