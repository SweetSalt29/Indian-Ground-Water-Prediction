import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np
from datetime import datetime

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Groundwater Level Analysis",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Load Data and Models
# ----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/groundwater_clean.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please ensure 'data/groundwater_clean.csv' exists.")
        return None

@st.cache_resource
def load_models():
    try:
        regressor = joblib.load("models/regression_model.pkl")
        encoder = joblib.load("models/encoder.pkl")
        anomaly_model = joblib.load("models/anomaly_model.pkl")
        return regressor, encoder, anomaly_model
    except FileNotFoundError as e:
        st.error(f"❌ Model file not found: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"❌ Error loading models: {e}")
        return None, None, None

df = load_data()
regressor, encoder, anomaly_model = load_models()

if df is None:
    st.stop()

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main-header {font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center;}
.sub-header {font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/000000/water.png", width=80)
st.sidebar.title("🌊 Groundwater Monitor")
page = st.sidebar.radio("Navigate to:", ["🏠 Home", "📈 Regression Analysis", "🚨 Anomaly Detection", "ℹ️ About"], index=0)
st.sidebar.markdown("---")
st.sidebar.info(f"📅 **Today:** {datetime.now().strftime('%B %d, %Y')}")

# ----------------------------
# HOME
# ----------------------------
if page == "🏠 Home":
    st.markdown("<div class='main-header'>💧 Groundwater Level Monitoring System</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>AI-Powered Analysis & Prediction Platform</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📍 Total Stations", len(df["station_name"].unique()))
    with col2: st.metric("🏛️ Districts Covered", len(df["district_name"].unique()))
    with col3: st.metric("🗺️ States Monitored", len(df["state_name"].unique()))
    with col4: st.metric("📊 Data Points", len(df))

# ----------------------------
# REGRESSION
# ----------------------------
elif page == "📈 Regression Analysis":
    st.markdown("<div class='main-header'>📈 Groundwater Level Prediction</div>", unsafe_allow_html=True)

    if regressor is None or encoder is None:
        st.error("⚠️ Model or encoder missing. Please ensure all files exist in 'models/'.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col1:
        state = st.selectbox("🏛️ Select State", sorted(df["state_name"].unique()))
    with col2:
        district = st.selectbox("📍 Select District", sorted(df[df["state_name"] == state]["district_name"].unique()))
    with col3:
        station = st.selectbox("🎯 Select Station", sorted(df[df["district_name"] == district]["station_name"].unique()))

    station_data = df[
        (df["state_name"] == state)
        & (df["district_name"] == district)
        & (df["station_name"] == station)
    ]

    if station_data.empty:
        st.warning("⚠️ No data available for this selection.")
        st.stop()

    # ✅ Extract required numeric features
    latitude = station_data["latitude"].iloc[0] if "latitude" in station_data.columns else 0
    longitude = station_data["longitude"].iloc[0] if "longitude" in station_data.columns else 0
    level_diff = station_data["level_diff"].iloc[-1] if "level_diff" in station_data.columns else 0

    # ✅ Create input dataframe
    input_df = pd.DataFrame({
        "state_name": [state],
        "district_name": [district],
        "station_name": [station],
        "latitude": [latitude],
        "longitude": [longitude],
        "level_diff": [level_diff],
        "year": [2024]
    })

    try:
        # Encode categorical variables
        input_df[["state_name", "district_name", "station_name"]] = encoder.transform(
            input_df[["state_name", "district_name", "station_name"]]
        )

        # ✅ Match column order to model
        if hasattr(regressor, "feature_names_in_"):
            input_df = input_df[regressor.feature_names_in_]

        # ✅ Predict groundwater level
        predicted_value = regressor.predict(input_df)[0]

    except Exception as e:
        st.error(f"❌ Prediction error: {e}")
        st.stop()

    # ✅ Plot trend with predicted 2024 value
    numeric_cols = station_data.select_dtypes(include=[np.number]).columns
    groundwater_col = numeric_cols[0]
    trend_data = station_data[["year", groundwater_col]].copy().sort_values("year")

    if 2024 not in trend_data["year"].values:
        trend_data = pd.concat([
            trend_data,
            pd.DataFrame({"year": [2024], groundwater_col: [predicted_value]})
        ], ignore_index=True)

    fig = px.line(trend_data, x="year", y=groundwater_col, markers=True, color_discrete_sequence=["#1f77b4"])
    fig.add_scatter(
        x=[2024], y=[predicted_value],
        mode='markers+text',
        marker=dict(size=12, color="#ff7f0e"),
        text=[f"{predicted_value:.2f} m"],
        textposition="top center"
    )
    st.plotly_chart(fig, use_container_width=True)



# ----------------------------
# ANOMALY DETECTION
# ----------------------------
elif page == "🚨 Anomaly Detection":
    st.markdown("<div class='main-header'>🚨 Anomaly Detection System</div>", unsafe_allow_html=True)

    if anomaly_model is None:
        st.error("⚠️ Anomaly model not found in 'models/'.")
        st.stop()

    st.sidebar.subheader("🎛️ Filter Options")
    selected_states = st.sidebar.multiselect("🏛️ Select States", sorted(df["state_name"].unique()), default=[])
    anomaly_threshold = st.sidebar.slider("🎯 Highlight Districts Above (%)", 0, 100, 20)
    run_button = st.sidebar.button("🔍 Run Analysis")

    if run_button:
        with st.spinner("Running anomaly detection..."):
            filtered_df = df[df["state_name"].isin(selected_states)] if selected_states else df

            try:
                # ✅ MANUALLY define the same features used during training
                model_features = [
                    "currentlevel",
                    "level_diff",
                    "latitude",
                    "longitude",
                    "year"
                ]

                # ✅ Check for missing columns
                missing = [f for f in model_features if f not in filtered_df.columns]
                if missing:
                    st.error(f"❌ Missing columns required by the anomaly model: {missing}")
                    st.stop()

                # ✅ Prepare data for prediction
                X = filtered_df[model_features]

                # ✅ Run predictions
                filtered_df["anomaly_label"] = anomaly_model.predict(X)
                filtered_df["Anomaly"] = filtered_df["anomaly_label"].map({1: "Normal", -1: "Anomalous"})

                # 📊 Summarize anomalies by district
                district_anomaly = (
                    filtered_df.groupby("district_name")["Anomaly"]
                    .apply(lambda x: (x == "Anomalous").mean() * 100)
                    .reset_index(name="Anomaly_Percentage")
                    .sort_values("Anomaly_Percentage", ascending=False)
                )

                # 🟢🟡🔴 Risk categorization
                district_anomaly["Status"] = district_anomaly["Anomaly_Percentage"].apply(
                    lambda x: "🔴 High Risk" if x >= anomaly_threshold 
                    else "🟡 Medium Risk" if x >= anomaly_threshold/2 
                    else "🟢 Low Risk"
                )

                st.subheader("📊 District Anomaly Summary")
                st.dataframe(
                    district_anomaly.style.format({"Anomaly_Percentage": "{:.2f}%"}),
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"❌ Error running anomaly detection: {e}")



# ----------------------------
# ABOUT
# ----------------------------
elif page == "ℹ️ About":
    st.markdown("<div class='main-header'>ℹ️ About This Application</div>", unsafe_allow_html=True)
    st.markdown("""
    This project uses **Machine Learning** to:
    - Predict groundwater levels for future years (Regression)
    - Detect abnormal patterns (Anomaly Detection)

    **Models Used:**
    - Random Forest Regressor
    - Isolation Forest (Anomaly Detection)
    """)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown("<div style='text-align:center;color:#777;'>💧 Developed by Aaryan | Powered by Streamlit & Scikit-learn</div>", unsafe_allow_html=True)
