import streamlit as st
import pandas as pd
from pathlib import Path

# --- Page setup ---
icon_path = Path(__file__).parent / "drone_icon.png"

st.set_page_config(
    page_title="Drone Design Calculator",
    page_icon=str(icon_path),   # use custom image
    layout="wide"
)

# --- Calculator function ---
def quadcopter_calculator(prop_diameter_inch, drone_weight_g, thrust_per_motor_g):
    prop_size_mm = prop_diameter_inch * 25.4
    arm_length_mm = (prop_size_mm * 1.1) / 2
    diag_frame_size = arm_length_mm * 2
    center_plate = arm_length_mm * 0.72
    total_diag = diag_frame_size + center_plate

    rotor_count = 4
    total_thrust = thrust_per_motor_g * rotor_count
    twr = total_thrust / drone_weight_g if drone_weight_g > 0 else 0

    # Format values as integers with comma separators
    return {
        "Propeller Diameter (mm)": f"{round(prop_size_mm):,}",
        "Arm Length (mm)": f"{round(arm_length_mm):,}",
        "Diagonal Frame (mm)": f"{round(diag_frame_size):,}",
        "Center Plate (mm)": f"{round(center_plate):,}",
        "Total Diagonal (mm)": f"{round(total_diag):,}",
        "Total Thrust (g)": f"{round(total_thrust):,}",
        "Thrust-to-Weight Ratio": f"{round(twr):,}"
    }

# --- UI ---
st.title("Drone Design Calculator")
st.markdown("Estimate thrust and frame dimensions for your quadcopter design.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔧 Inputs")
    prop_diameter = st.number_input("Propeller Diameter (inches)", min_value=1.0, value=10.0)
    drone_weight = st.number_input("Drone Weight (g)", min_value=100, value=1500)
    thrust_per_motor = st.number_input("Thrust per Motor (g)", min_value=100, value=1000)
    calculate = st.button("🚀 Calculate")

with col2:
    st.subheader("📊 Results")
    if calculate:
        results = quadcopter_calculator(prop_diameter, drone_weight, thrust_per_motor)
        df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
        st.table(df)
    else:
        st.info("Enter your inputs and click **Calculate** to see results.")

st.markdown("---")
st.caption("⚡ Built with Streamlit")
