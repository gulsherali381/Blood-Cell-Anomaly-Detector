import pandas as pd
import streamlit as st
import requests
from datetime import datetime

API_url = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Blood Cell Anomaly Detector",
    page_icon="🩸",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
   .stApp {
        background-color: #010002;
        color: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
        border-right: 2px solid #8715DB;
    }
    h1, h2, h3 {
         color: #8715DB;
    }
    .stButton button {
        background-color: #8715DB;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #6d10ae;
    }
    .stFormSubmitButton button {
        background-color: #8715DB;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    .stFormSubmitButton button:hover {
        background-color: #6d10ae;
    }
    /* --- Download Button Color Fix --- */
    .stDownloadButton button {
        background-color: #8715DB !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    .stDownloadButton button:hover {
        background-color: #6d10ae !important;
    }
    /* --------------------------------- */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: #8715DB !important;
        font-weight: 600;
    }
    .hero-box {
        background: linear-gradient(135deg, #1a0530, #8715DB);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .disclaimer-box {
        background-color: #1a1a1a;
        border: 1px solid #8715DB;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    .result-card {
        background-color: #1a1a1a;
        border: 2px solid #8715DB;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE ------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero-box">
    <h1 style="color:white;">🧬 Cellular Irregularity Scanner</h1>
    <p style="color: #dcd0ea;"> AI-Powered Blood Cell Anomaly screening using Isolation Forest</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
        ⚠️ <b>Disclaimer: </b> This tool is for research/educational purposes only and is not a medical diagnosis.
         Please consult a qualified lab professional for any medical decisions.
</div>
""", unsafe_allow_html=True)


# ------------------ TABS ------------------
tab1, tab2, tab3, tab4 = st.tabs(["🧪 Scan", "📈 Insights", "📦 Bulk Scan", "🗂️ Log"])

with tab1:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("🔬 Patient Information")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            patient_id = st.text_input("Patient ID", value="MRN-2026-001")
            patient_name = st.text_input("Patient Full Name ", value="John Doe")

        with col_p2:
            patient_age = st.number_input("Age", min_value=0, max_value=120, value=32)
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.markdown("---")
        st.subheader("🔬 Cell Feature Input")
        with st.form("Scan_form"):
            cell_type = st.selectbox(
                "Cell Type", [
                    'Artefact', 'Basophil', 'Blast_Cell', 'Elliptocyte', 'Eosinophil',
                    'Hypersegmented_Neutrophil', 'Lymphocyte', 'Monocyte', 'Neutrophil',
                    'Normal_RBC', 'Platelet', 'Prolymphocyte', 'Reactive_Lymphocyte',
                    'Schistocyte', 'Sickle_Cell', 'Smudge_Cell', 'Spherocyte',
                    'Target_Cell', 'Toxic_Granulation'
                ])
            c1, c2 = st.columns(2)
            with c1:
                cell_diameter_um = st.number_input("Cell Diameter (um)", min_value=0.1, value=10.0)
                nucleus_area_pct = st.number_input("Nucleus Area%", min_value=0.0, max_value=100.0, value=50.0)
                chromatin_density = st.number_input("Chromatin Density", min_value=0.0, value=0.4)
                cytoplasm_ratio = st.number_input("Cytoplasm Ratio", min_value=0.0, value=0.4)
                circularity = st.number_input("Circularity", min_value=0.0, max_value=1.0, value=0.8)
                eccentricity = st.number_input("Eccentricity", min_value=0.0, max_value=1.0, value=0.4)
                granularity_score = st.number_input("Granularity Score", min_value=0.0, value=2.0)
            with c2:
                lobularity_score = st.number_input("Lobularity Score", min_value=0.0, value=3.0)
                membrane_smoothness = st.number_input("Membrane Smoothness", min_value=0.0, max_value=1.0, value=0.8)
                cell_area_px = st.number_input("Cell Area(px)", min_value=1, value=300)
                perimeter_px = st.number_input("Perimeter(px)", min_value=1, value=60)
                mean_r = st.number_input("Mean Red", min_value=0, max_value=255, value=200)
                mean_g = st.number_input("Mean Green", min_value=0, max_value=255, value=150)
                mean_b = st.number_input("Mean Blue", min_value=0, max_value=255, value=180)
                stain_intensity = st.number_input("Stain Intensity", min_value=0.0, value=0.5)

            threshold = st.slider("Sensitivity", min_value=-0.2, max_value=0.2, value=0.0, step=0.01)
            submitted = st.form_submit_button("🔍 Run Scan")

        if submitted:
            requests.get(f"{API_url}/set-threshold", params={"value": threshold})

            payload = {
                "patient_id": patient_id,
                "patient_name": patient_name,
                "patient_age": patient_age,
                "patient_gender": patient_gender,
                "cell_type": cell_type,
                "cell_diameter_um": cell_diameter_um,
                "nucleus_area_pct": nucleus_area_pct,
                "chromatin_density": chromatin_density,
                "cytoplasm_ratio": cytoplasm_ratio,
                "circularity": circularity,
                "eccentricity": eccentricity,
                "granularity_score": granularity_score,
                "lobularity_score": lobularity_score,
                "membrane_smoothness": membrane_smoothness,
                "cell_area_px": cell_area_px,
                "perimeter_px": perimeter_px,
                "mean_r": mean_r,
                "mean_g": mean_g,
                "mean_b": mean_b,
                "stain_intensity": stain_intensity
            }

            try:
                response = requests.post(f"{API_url}/predict", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("Prediction")
                    score = result.get("Score", 0.0)

                    st.session_state["history"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "patient_id": patient_id,
                        "patient_name": patient_name,
                        "cell_type": cell_type,
                        "prediction": prediction,
                        "score": score
                    })

                    with col_right:
                        st.subheader("📊 Scan Result")
                        color = "#ff4b4b" if prediction == "Anomaly" else "#00c853"
                        st.markdown(f"""
                        <div class="result-card">
                            <h3 style="color: {color}">{prediction.upper()}</h3>
                            <p style="font-size:2rem; font-weight:bold;">{score:.4f}</p>
                            <p>Anomaly Score</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(f"Prediction failed. Server status code: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend server! Make sure uvicorn is running on port 8000.")

# ------------------ TAB2 Insights------------------
with tab2:
    st.subheader("📈 Dataset Insights")
    try:
        df = pd.read_csv("blood_cell_anomaly_detection.csv")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cells", len(df))
        c2.metric("Anomaly Rate", f"{df['anomaly_label'].mean() * 100:.1f}%")
        c3.metric("Avg Diameter", f"{df['cell_diameter_um'].mean():.2f}um")
        c4.metric("Avg Circularity", f"{df['circularity'].mean():.2f}")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("Normal vs Anomaly Distribution")
            counts = df['anomaly_label'].map({0: "Normal", 1: "Anomaly"}).value_counts()
            st.bar_chart(counts)

        with col_b:
            st.write("Circularity Distribution")
            st.bar_chart(df['circularity'])
    except FileNotFoundError:
        st.warning("The dataset file was not found in this folder.")

# ------------------ TAB 3 : BULK SCAN ------------------
with tab3:
    st.subheader("📦 Bulk Cell Scan")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        st.write("Preview:", batch_df.head())

        if st.button("Run Bulk Scan"):
            result = []
            progress = st.progress(0)
            total = len(batch_df)

            for i, row in batch_df.iterrows():
                payload = row.to_dict()
                try:
                    response = requests.post(f"{API_url}/predict", json=payload)
                    if response.status_code == 200:
                        res = response.json()
                        result.append({"Prediction": res["Prediction"], "Score": res["Score"]})

                        # History mein bhi save karo
                        st.session_state["history"].append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "cell_type": row.get("cell_type", "N/A"),
                            "prediction": res["Prediction"],
                            "score": res["Score"]
                        })
                    else:
                        result.append({"Prediction": "Error", "Score": None})
                except:
                    result.append({"Prediction": "Error", "Score": None})
                progress.progress((i + 1) / total)

            results_df = pd.concat([batch_df, pd.DataFrame(result)], axis=1)
            st.dataframe(results_df)
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Results CSV", csv, "scan_results.csv", "text/csv")

# ------------------ TAB 4: LOG (History) ------------------
with tab4:
    st.subheader("🗂️ Scan Log")
    history = st.session_state["history"]
    if len(history) == 0:
        st.info("No scans have been performed yet.")
    else:
        history_df = pd.DataFrame(history)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scans", len(history_df))
        c2.metric("Avg Score", f"{history_df['score'].mean():.4f}")
        c3.metric("Most Common", history_df['prediction'].mode()[0])

        st.dataframe(history_df)

        st.write("Score Over Time")
        st.line_chart(history_df.set_index("timestamp")["score"])