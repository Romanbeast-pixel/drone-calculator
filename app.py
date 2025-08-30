import streamlit as st
import pandas as pd

# --- Page setup ---
st.set_page_config(
    page_title="Drone Design Calculator",
    page_icon="🛩️",
    layout="wide"
)

# --- Calculator function ---
def quadcopter_calculator(prop_size_inch, drone_weight_g, thrust_per_motor_g,
                          battery_voltage, battery_capacity_mah,
                          motor_kv, rotor_count):

    prop_size_mm = prop_size_inch * 25.4
    arm_length_mm = (prop_size_mm * 1.1) / 2
    diag_frame_size = arm_length_mm * 2
    center_plate = arm_length_mm * 0.72
    total_diag = diag_frame_size + center_plate

    total_thrust = thrust_per_motor_g * rotor_count
    twr = total_thrust / drone_weight_g if drone_weight_g > 0 else 0

    power_per_motor = motor_kv * battery_voltage * 0.001
    total_power = power_per_motor * rotor_count
    current_draw = total_power / battery_voltage if battery_voltage > 0 else 0
    battery_capacity_ah = battery_capacity_mah / 1000
    flight_time = (battery_capacity_ah / current_draw) * 60 * 0.8 if current_draw > 0 else 0
    esc_rating = round(current_draw / rotor_count * 1.3) if rotor_count > 0 else 0

    return {
        "Propeller Size (mm)": round(prop_size_mm, 2),
        "Arm Length (mm)": round(arm_length_mm, 2),
        "Diagonal Frame (mm)": round(diag_frame_size, 2),
        "Center Plate (mm)": round(center_plate, 2),
        "Total Diagonal (mm)": round(total_diag, 2),
        "Total Thrust (g)": total_thrust,
        "Thrust-to-Weight Ratio": round(twr, 2),
        "Power per Motor (W)": round(power_per_motor, 2),
        "Total Power (W)": round(total_power, 2),
        "Current Draw (A)": round(current_draw, 2),
        "Est. Flight Time (min)": round(flight_time, 2),
        "ESC Rating Suggestion (A)": esc_rating
    }

# --- UI ---
st.title("🛩️ Drone Design Calculator")
st.markdown("Estimate thrust, power, and flight time for your multirotor design.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔧 Inputs")
    prop_size = st.number_input("Propeller Size (inches)", min_value=1.0, value=10.0)
    drone_weight = st.number_input("Drone Weight (g)", min_value=100, value=1500)
    thrust_per_motor = st.number_input("Thrust per Motor (g)", min_value=100, value=1000)
    battery_voltage = st.number_input("Battery Voltage (V)", min_value=3.0, value=14.8)
    battery_capacity = st.number_input("Battery Capacity (mAh)", min_value=500, value=5200)
    motor_kv = st.number_input("Motor KV Rating", min_value=100, value=1000)
    rotor_count = st.selectbox("Number of Rotors", [4, 6, 8], index=0)

    calculate = st.button("🚀 Calculate")

with col2:
    st.subheader("📊 Results")
    if calculate:
        results = quadcopter_calculator(
            prop_size, drone_weight, thrust_per_motor,
            battery_voltage, battery_capacity,
            motor_kv, rotor_count
        )
        df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
        st.table(df)
    else:
        st.info("Enter your inputs and click **Calculate** to see results.")

# --- Footer ---
st.markdown("---")
st.caption("⚡ Built with Streamlit")
