import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set page configuration
st.set_page_config(page_title="🔋 Battery Dashboard", layout="wide")

# ---------- Function Definitions ----------

def generate_cells():
    cells = {}
    for i in range(1, 9):
        cell_type = random.choice(["lfp", "nmc"])
        voltage = 3.2 if cell_type == "lfp" else 3.6
        min_v = 2.8 if cell_type == "lfp" else 3.2
        max_v = 3.6 if cell_type == "lfp" else 4.0
        current = 0.6
        temp = round(random.uniform(25, 40), 1)
        capacity = round(voltage * current, 2)

        cells[f"cell_{i}_{cell_type}"] = {
            "type": cell_type,
            "voltage": voltage,
            "min_voltage": min_v,
            "max_voltage": max_v,
            "current": current,
            "temp": temp,
            "capacity": capacity
        }
    return cells

def update_cells(cells):
    for cell in cells.values():
        delta_v = random.uniform(-0.05, 0.05)
        cell["voltage"] = round(
            min(max(cell["voltage"] + delta_v, cell["min_voltage"]), cell["max_voltage"]), 2
        )
        cell["temp"] = round(cell["temp"] + random.uniform(-0.3, 0.3), 1)

# ---------- Streamlit UI Starts Here ----------

st.title("🔋 Battery Cell Monitoring System")

# Sidebar navigation
page = st.sidebar.selectbox("📂 Menu", ["Dashboard", "Live Simulation"])

# Session state for storing cell data
if "cells" not in st.session_state:
    st.session_state.cells = generate_cells()

cells = st.session_state.cells
df = pd.DataFrame(cells).T

if page == "Dashboard":
    st.header("📊 Cell Data Overview")
    st.dataframe(df)

    st.subheader("🔌 Voltage Distribution")
    fig, ax = plt.subplots()
    ax.bar(df.index, df["voltage"], color="#8bd3dd")
    ax.set_ylabel("Voltage (V)")
    ax.set_xlabel("Cells")
    ax.set_title("Voltage of Each Cell")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("🌡️ Temperature Overview")
    fig2, ax2 = plt.subplots()
    ax2.plot(df.index, df["temp"], marker="o", color="#f3b0c3")
    ax2.set_ylabel("Temperature (°C)")
    ax2.set_title("Cell Temperature")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

elif page == "Live Simulation":
    st.header("⚡ Real-time Charging/Discharging")

    placeholder = st.empty()

    if "sim_running" not in st.session_state:
        st.session_state.sim_running = False

    col1, col2 = st.columns(2)
    if col1.button("▶ Start Simulation"):
        st.session_state.sim_running = True

    if col2.button("⏹ Stop"):
        st.session_state.sim_running = False

    while st.session_state.sim_running:
        update_cells(cells)
        df = pd.DataFrame(cells).T

        with placeholder.container():
            cols = st.columns(4)
            for idx, (name, cell) in enumerate(cells.items()):
                color = "🟢"
                if cell["temp"] > 35:
                    color = "🔴"
                elif cell["temp"] > 30:
                    color = "🟠"

                cols[idx % 4].metric(
                    label=f"{name} {color}",
                    value=f"{cell['voltage']} V",
                    delta=f"{cell['temp']} °C"
                )
        time.sleep(1)
        st.rerun()
