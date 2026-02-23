"""
GreenArb - Command Center Visualization "The Big Reveal"
Provides real-time graphical insights into the hardware telemetry,
EAA decision logs, and carbon scores. Deployment-ready.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import os

st.set_page_config(layout="wide", page_title="GreenArb Command Center")

LOG_OUTPUT = r"C:\Users\K.Visagan\.gemini\antigravity\scratch\GreenArb\decision_logic\eaa_logs.csv"

def get_data():
    if not os.path.exists(LOG_OUTPUT):
        return pd.DataFrame()
    try:
        df = pd.read_csv(LOG_OUTPUT)
        return df.tail(50)
    except Exception:
        return pd.DataFrame()

st.title("🌱 GreenArb Command Center: Live Execution Loop")
st.markdown("Mech-Sympathy Integration: AMD Hardware ↔ Palantir OS | Final Pitch")

placeholder = st.empty()

while True:
    df = get_data()
    
    if df.empty or 'final_profit' not in df.columns:
        with placeholder.container():
            st.warning("Awaiting Initial AIP Data Stream & Payload...")
        time.sleep(1.0)
        continue

    latest = df.iloc[-1]
    
    with placeholder.container():
        # FOUNDER'S SIGNATURE WIDGET
        total_co2_saved = (df['saved_watts'].sum() / 1000) * 0.42 # arbitrary proxy for CO2 Kg
        total_profit_generated = df['final_profit'].sum()
        
        st.markdown(f"### 🖋️ Founder's Signature")
        st.success(f"**Session ESG Impact**: {total_co2_saved:.4f} kg CO2 Avoided | **Session Alpha Generated**: ₹{total_profit_generated:.2f}")
        st.markdown("---")
        
        # Top Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="MI325X GPU Status", value=f"{latest['gpu_power_w']:.1f} W", delta=f"{latest['gpu_temp_c']:.1f} °C", delta_color="inverse")
            st.caption(f"**VRAM BW (Active):** {latest.get('vram_bandwidth_gbs', 0)} GB/s | **Eff:** {latest.get('vram_efficiency_pct', 0):.1f}%")
            
        with col2:
            st.metric(label="TN Grid Intensity", value=f"{latest['carbon_intensity']:.1f} gCO2/kWh")
            st.caption(f"**Carbon Tax Penalty:** ₹{latest.get('carbon_tax', 0):.2f}")
            
        with col3:
            ga = latest['green_alpha_score']
            color = "green" if ga >= 60 else ("orange" if ga >= 40 else "red")
            st.markdown(f"**GreenAlpha Score**<br><h2 style='color: {color}; margin-top: -10px;'>{ga:.1f} / 100</h2>", unsafe_allow_html=True)
            
        with col4:
            st.metric(label="Carbon Credit Revenue", value=f"₹{latest.get('carbon_credit_value', 0):.2f}")
            st.caption(f"**Watts Saved Accumulator:** {df['saved_watts'].sum():.1f} W")
            
        st.markdown("---")
        
        # Sovereign Matrix Failover & Live Spread
        col_fail, col_spread1, col_spread2, col_spread3 = st.columns(4)
        
        with col_fail:
            st.markdown("#### Sovereign Failover Status")
            if latest['carbon_intensity'] > 450:
                st.error("🚀 ACTIVE: EU-SOUTH-MADRID (Spain) | TN Grid > 450g/kWh")
            else:
                st.info("✅ PRIMARY: AP-SOUTH-CHN (Chennai) | Optimal Grid")
            st.caption("Standby: US-EAST-NJ (Virginia)")
            
        with col_spread1:
            st.metric(label="Live Spread (INR Net)", value=f"₹{latest.get('net_spread_profit', 0):.2f}")
        with col_spread2:
            st.metric(label="INFY NSE", value=f"₹{latest.get('infy_nse', 0):.2f}")
        with col_spread3:
            st.metric(label="INFY ADR (USD > INR)", value=f"${latest.get('infy_adr', 0):.2f} @ ₹{latest.get('usd_inr', 0):.2f}")

        st.markdown("---")
        
        # Charts Row
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("24-Hour Carbon-Alpha Curve (Avoided Dirty Alpha)")
            fig1 = go.Figure()
            
            fig1.add_trace(go.Scatter(x=df['time_str'], y=df['net_spread_profit'], mode='lines', name='Dirty Alpha (Gross Spread)', line=dict(color='orange')))
            fig1.add_trace(go.Scatter(x=df['time_str'], y=df['final_profit'], mode='lines', name='Green Alpha (Net Revenue)', line=dict(color='green')))
            fig1.add_trace(go.Scatter(x=df['time_str'], y=df['carbon_tax'], mode='lines', name='Carbon Tax Penalty', line=dict(color='red', dash='dot')))
            
            executions = df[df['action'] == 'EXECUTE_TRADE']
            fig1.add_trace(go.Scatter(x=executions['time_str'], y=executions['final_profit'], mode='markers', name='Execute (Burst 1.8μs)', marker=dict(color='green', size=10)))
            
            fig1.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0), yaxis_title="INR (₹)")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_chart2:
            st.subheader("AMD Thermal & Power Gauge (Burst Mode)")
            gauge_color = "red" if latest['gpu_power_w'] > 350 else "darkgreen"
            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = latest['gpu_power_w'],
                title = {'text': "MI325X Wattage"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 500]},
                    'bar': {'color': gauge_color},
                    'steps' : [
                        {'range': [0, 250], 'color': "lightgreen"},
                        {'range': [250, 400], 'color': "yellow"},
                        {'range': [400, 500], 'color': "red"}],
                    'threshold' : {'line': {'color': "purple", 'width': 4}, 'thickness': 0.75, 'value': 400}
                }
            ))
            fig2.update_layout(height=400, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig2, use_container_width=True)
            
        # Recent logs table
        st.subheader("Immutable Provenance Ledger (Last 5 Ticks)")
        st.dataframe(df[['time_str', 'gpu_power_w', 'vram_efficiency_pct', 'carbon_tax', 'carbon_credit_value', 'final_profit', 'action']].tail(5).sort_index(ascending=False), use_container_width=True)

    time.sleep(0.5)
